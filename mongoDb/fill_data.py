"""@package mongoDb
Generate dummy data
"""

import random
import string
from datetime import datetime

from classes.db_connect import DbConnect
from models import Condition, Parameter, Subdetector, Source


def tag_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generates random tags
    :param size: Size of the tag
    :param chars: The ASCII characters contained in the tag
    :return: Randomly generated tag name
    """
    return ''.join(random.choice(chars) for _ in range(size))


DbConnect.get_connection("conditionsDB")

sources = ["Alignment", "Calibration", "Central Data Acquisition"]

subdetectors = ["Target Tracker", "Muon", "hcal", "ecal", "Veto Taggers", "BckGr Tagger", "Drift Tubes"]

gain = ["Gain", [["EtInCenter", "10.*GeV 10.*GeV 10.*GeV"], ["EtSlope", "7.*GeV  7.*GeV  7.*GeV"], ["PedShift", "0.4"],
                 ["PinPedShift", "1.1"], ["CoherentNoise", "0.3"], ["IncoherentNoise", "1.2"],
                 ["StochasticTerm", "0.10"], ["GainError", "0.01"]]]
cham01 = ["Cham001", [["dPosXYZ", "0 0 0"], ["dRotXYZ", "0 0 0"]]]
cham02 = ["Cham002", [["dPosXYZ", "1 1 1"], ["dRotXYZ", "1 1 1"]]]
cham03 = ["Cham003", [["dPosXYZ", "2 2 2"], ["dRotXYZ", "2 2 2"]]]
temperature = ["GlobalTemperature", [["temperature", "100C"]]]

conditions = [gain, cham01, cham02, cham03, temperature]

for s in sources:
    src = Source(name=s.__str__())

    src.save()

sources_obj = Source.objects.all()

for s in subdetectors:

    sub = Subdetector(name=s.__str__())

    for c in conditions:

        count = len(sources_obj)

        random_index = random.randint(0, count - 1)

        condition = Condition(name=c[0], iov=datetime.now(), tag=tag_generator(),
                              source=sources_obj[random_index])

        params = c[1]

        for p in params:
            condition.parameters.append(Parameter(name=p[0], value=p[1], iov=datetime.now()))

        sub.conditions.append(condition)

        sub.save()
