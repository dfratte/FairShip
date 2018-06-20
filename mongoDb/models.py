from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ComplexDateTimeField
from bson.timestamp import Timestamp

class Parameter(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    value = StringField(max_length=1000, null=True)

class Condition(EmbeddedDocument):
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    tag = StringField(max_length=1000, null=True)
    parameters = EmbeddedDocumentListField(Parameter)

class Subdetector(Document):
    name = StringField(max_length=1000, null=True)
    conditions = EmbeddedDocumentListField(Condition)
