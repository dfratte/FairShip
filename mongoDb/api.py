"""@package mongoDb
ConditionsDB API
"""
from classes.db_connect import DbConnect
from models import Subdetector

class API(object):

    def __init__(self):
        DbConnect.get_connection('conditionsDB')

    @staticmethod
    def list_subdetectors():
        return Subdetector.objects()

    @staticmethod
    def show_subdetector(searched_name):
        return Subdetector.objects(name=searched_name).first()

    @staticmethod
    def show_subdetector_conditions(searched_name):
        return API.show_subdetector(searched_name).conditions

    @staticmethod
    def show_subdetector_condition(searched_name, searched_condition):
        return Subdetector.objects(name=searched_name).first().conditions.filter(name=searched_condition).first()

    @staticmethod
    def show_subdetector_iov(searched_name, searched_iov):
        # Subdetector.objects(name=searched_name).first().conditions.objects(iov__lte=searched_iov).first()
        # Condition.objects(subdetects=asdas && iov__lte=5 && iov__gte = 3)

        if "-" not in searched_iov:
            return [self.show_subdetector_conditions(searched_name).filter(iov=searched_iov).first()]

        else:
            x, y = searched_iov.split("-")
            myIOVs = []

            for i in range(int(x), int(y) + 1):
                myIOV = self.show_subdetector_conditions(searched_name).filter(iov=i).first()
                myIOVs.append(myIOV)

            return myIOVs

    @staticmethod
    def add_subdetector(new_subdetector):
        try:
            Subdetector(**new_subdetector).save()
        except ValueError:
            return -1

        return 1
