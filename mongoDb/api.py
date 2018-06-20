# from mongoengine import connect
from models import Subdetector, Condition
from classes.db_connect import DB_connect

connect = DB_connect()
connect.dbname('conditionsDB')


class API:

    def list_subdetectors(self):
        return Subdetector.objects()

    def show_subdetector(self, searched_name):
        # return Subdetector.objects(name=searched_name).first()
        return Subdetector.objects(name=searched_name).first()

    def show_subdetector_conditions(self, searched_name):
        # return self.show_subdetector(searched_name).values_list('conditions')

        return Subdetector.objects(name=searched_name).values_list('conditions')

    def show_subdetector_condition(self, searched_name, searched_condition):
        return Subdetector.objects(name=searched_name).first().conditions.filter(name=searched_condition).first()

    def show_subdetector_iovs(self, searched_name, searched_iovs):
        return Subdetector.objects(name=searched_name).first().conditions.filter(iov=searched_iovs).first()

    def show_subdetector_iov(self, searched_name, searched_iov):

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

    # def add_subdetector_iov(self, searched_name, searched_iov):
