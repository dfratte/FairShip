import random

from mongoengine import connect

from models import *

connect(db='cernSimple',
        # user='',
        # password='',
        host='localhost',
        port=27017
        )

for i in range(1, 100):
    sub = Subdetector(name='subdetector' + i.__str__())

    for c in range(1, 10):
        c = Condition(name='condition_' + c.__str__(), iov=c, tag='tag_' + c.__str__())

        for j in range(1, 20):
            seq = random.randint(1, 1000)
            c.parameters.append(Parameter(name='param_' + seq.__str__(), value='value_' + seq.__str__(), iov=seq))

        sub.conditions.append(c)
        sub.save()
