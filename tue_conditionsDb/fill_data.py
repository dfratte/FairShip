"""@package tue_conditionsDb
Generate dummy data
"""

import datetime
import random

from classes.db_connect import DbConnect
from models import Condition, Parameter, Subdetector, Source, GlobalTag


# def tag_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     """
#     Generates random tags
#     :param size: Size of the tag
#     :param chars: The ASCII characters contained in the tag
#     :return: Randomly generated tag name
#     """
#     return ''.join(random.choice(chars) for _ in range(size))

def tag_generator(subdetector_name, condition_name):
    """
    Generates a tag from the name of the subdetector, the condition and the current daytime
    :param subdetector_name: Name of subdetector (string)
    :param condition_name: Name of condition (string)
    :return: The name of the tag (e.g. Muon_Alignment_2018-06-28 15:52:54.108437)
    """
    return subdetector_name + '_' + condition_name + '_' + str(datetime.datetime.now())

connection_dict = {'db_name': 'conditionsDB', 'user': None, 'password': None, 'host': "localhost", 'port':27017}

DbConnect.delete_db(connection_dict)
DbConnect.get_connection(connection_dict)

global_tags = ["Gain-June-26", "GlobalTemperature-Muon-ecal"]

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

for g in global_tags:
    global_tag = GlobalTag(name=g.__str__())

    global_tag.save()

for s in sources:
    src = Source(name=s.__str__())

    src.save()

sources_obj = Source.objects.all()

for s in subdetectors:

    sub = Subdetector(name=s.__str__())
    until_days = -4
    for c in conditions:

        count = len(sources_obj)

        random_index = random.randint(0, count - 1)

        since_date = datetime.datetime.now() - datetime.timedelta(days=7)
        until_date = datetime.datetime.now() + datetime.timedelta(days=until_days)

        condition = Condition(name=c[0], tag=tag_generator(s, c[0]), since=since_date,
                              until=until_date, source=sources_obj[random_index])
        until_days += 1

        params = c[1]

        for p in params:
            condition.parameters.append(Parameter(name=p[0], value=p[1]))

        sub.conditions.append(condition)

        sub.save()
