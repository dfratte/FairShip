"""@package mongoDb
ConditionsDB API
"""
from classes.db_connect import DbConnect
from models import Subdetector

DbConnect.get_connection('conditionsDB')


class API(object):

    def list_subdetectors(self):
        return Subdetector.objects()

    def show_subdetector(self, searched_name):
        return Subdetector.objects(name=searched_name).first()

    def show_subdetector_conditions(self, searched_name):
        return self.show_subdetector(searched_name).conditions

    def show_subdetector_condition(self, searched_name, searched_condition):
        return self.show_subdetector_conditions(searched_name).filter(name=searched_condition).first()

    def show_subdetector_iov(self, searched_name, searched_iov):
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

    def add_subdetector(self, subdetector_name):
        Subdetector(name=subdetector_name).save()
        return 'New subdetector added!'
