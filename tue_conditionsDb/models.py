"""@package mongoDb
MongoDb Models
"""
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ComplexDateTimeField, \
    ReferenceField


# TODO Review the class definitions (Parameter, Source, Condition, Subdetector)

class GlobalTag(Document):
    """
    GlobalTag
    """
    ##
    # @var name
    # Name of the Global Tag
    name = StringField(max_length=1000, null=True)

class Source(Document):
    """
    Source
    """
    ##
    # @var name
    # Name of the Source
    name = StringField(max_length=1000, null=True)


class Parameter(EmbeddedDocument):
    """
    Parameter refers to the specific condition of a subdetector e.g. Temperature
    """
    ##
    # @var name
    # Name of the Parameter
    # @var iov
    # Interval of Validity
    # @var value
    # Value of the Parameter
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    value = StringField(max_length=1000, null=True)


class Condition(EmbeddedDocument):
    """
    It refers to the setup and configuration of specific instrumentation utilized for carrying out certain
    HEP experiment.
    """
    ##
    # @var name
    # Name of the Condition
    # @var iov
    # Interval of Validity
    # @var tag
    # Tag of the Condition
    # @var parameters
    # Collection of parameters related to that Condition
    # @var source
    # Source used to group Conditions
    name = StringField(max_length=1000, null=True)
    iov = ComplexDateTimeField(null=True)
    tag = StringField(max_length=1000, null=True)
    parameters = EmbeddedDocumentListField(Parameter)
    since = ComplexDateTimeField(null=True)
    until = ComplexDateTimeField(null=True)
    source = ReferenceField(Source)
    global_tag = ReferenceField(GlobalTag)


class Subdetector(Document):
    """
    Components in which a Detector can be broken down to.
    """
    ##
    # @var name
    # Name of the Subdetector
    # @var conditions
    # Conditions evaluated by the Subdetector
    name = StringField(max_length=1000, null=True)
    conditions = EmbeddedDocumentListField(Condition)
