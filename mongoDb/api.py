from mongoengine import connect
from models import Subdetector

connect(db='cernSimple',
        # user='',
        # password='',
        host='localhost',
        port=27017
        )


def list_subdetectors():
    return Subdetector.objects()


def show_subdetector(searched_name):
    return Subdetector.objects(name=searched_name)

def show_subdetector_condition(searched_name):
    return 0