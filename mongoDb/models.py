"""@package mongoDb
MongoDb Models
"""
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ComplexDateTimeField, \
    ReferenceField

class Source(Document):
    name = StringField(max_length=1000, null=True)


class Parameter(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    value = StringField(max_length=1000, null=True)


class Condition(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    tag = StringField(max_length=1000, null=True)
    parameters = EmbeddedDocumentListField(Parameter)
    source = ReferenceField(Source)


class Subdetector(Document):
    name = StringField(max_length=1000, null=True)
    conditions = EmbeddedDocumentListField(Condition)
