from models import Subdetector
from classes.db_connect import DB_connect

class API(object):

    def __init__(self):
        connect = DB_connect()
        connect.dbname('conditionsDB')

    @staticmethod
    def list_subdetectors():
        return Subdetector.objects()

    @staticmethod
    def show_subdetector(searched_name):
        return Subdetector.objects(name=searched_name).first()

    def show_subdetector_conditions(self, searched_name):
        return self.show_subdetector(searched_name).conditions

    @staticmethod
    def show_subdetector_condition(searched_name, searched_condition):
        return Subdetector.objects(name=searched_name).first().conditions.filter(name=searched_condition).first()

    @staticmethod
    def show_subdetector_iov(searched_name, searched_iov):
        # Subdetector.objects(name=searched_name).first().conditions.objects(iov__lte=searched_iov).first()
        # Condition.objects(subdetects=asdas && iov__lte=5 && iov__gte = 3)

        if "-" not in searched_iov:
            return [Subdetector.objects(name=searched_name).first().conditions.filter(iov=searched_iov).first()]

        else:

            x, y = searched_iov.split("-")
            myIOVs = []

            for i in range(int(x), int(y) + 1):
                myIOV = Subdetector.objects(name=searched_name).first().conditions.filter(iov=i).first()
                myIOVs.append(myIOV)

            # print myIOVs
            # return r.json()['conditions']
            return myIOVs

    @staticmethod
    def add_subdetector(subdetector_name):
        Subdetector(name=subdetector_name).save()
        return 'New subdetector added!'
