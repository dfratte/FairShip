import random

from models import *
from mongoengine import *

connect(db='cernSimple',
        # user='',
        # password='',
        host='localhost',
        port=27017
        )

for i in range(1):
    sub = Subdetector(name='subdetector' + i.__str__())

    for c in range(2):
        c = Condition(name='condition_' + c.__str__(), iov=c, tag='tag_' + c.__str__())

        for j in range(3):
            seq = random.randint(1, 1000)
            c.parameters.append(Parameter(name='param_' + seq.__str__(), value='value_' + seq.__str__(), iov=seq))

        sub.conditions.append(c)
        sub.save()


class Parameter(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = LongField(null=True)
    value = StringField(max_length=1000, null=True)


class Condition(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = LongField(null=True)
    tag = StringField(max_length=1000, null=True)
    parameters = EmbeddedDocumentListField(Parameter)


class Subdetector(Document):
    name = StringField(max_length=1000, null=True)
    conditions = EmbeddedDocumentListField(Condition)
