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


def show_subdetector_conditions(searched_name):
    return show_subdetector(searched_name).values_list('conditions')
    # return Subdetector.objects(name=searched_name).values_list('conditions')


def show_subdetector_condition(searched_name, searched_condition):
    return Subdetector.objects(name=searched_name).first().conditions.filter(name=searched_condition).first()
