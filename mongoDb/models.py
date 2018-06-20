from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, LongField


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
