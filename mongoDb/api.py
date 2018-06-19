from mongoengine import connect
from models import Subdetector

connect(db='cernSimple',
        # user='',
        # password='',
        host='localhost',
        port=27017
        )


def list_subdetectors():
    for sd in Subdetector.objects:
        print(sd.name)
    print "Count: ", len(Subdetector.objects())


def show_subdetector(searched_name):
    print Subdetector.objects(name=searched_name).to_json()
