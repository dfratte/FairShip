# from mongoengine import connect
from models import Subdetector
# from mongoengine.queryset.visitor import Q
from classes.db_connect import DB_connect

connect = DB_connect()
connect.dbname('cernSimple')

class API:

    def list_subdetectors(self):
        return Subdetector.objects()


    def show_subdetector(self, searched_name):
        return Subdetector.objects(name=searched_name).first()


    def show_subdetector_conditions(self, searched_name):
        return self.show_subdetector(searched_name).values_list('conditions')

        # return Subdetector.objects(name=searched_name).values_list('conditions')


    def show_subdetector_condition(self, searched_name, searched_condition):
        # return Subdetector.objects(name=searched_name).first().conditions.filter(name=searched_condition).first()
        return Subdetector.objects(name=searched_name).first().conditions.filter(iov=searched_condition).first()


    def show_subdetector_iovs(self, searched_name, searched_iovs):
        return Subdetector.objects(name=searched_name).first().conditions.filter(iov=searched_iovs).first()


    def show_subdetector_iov(self, searched_name, searched_iov):
        return Subdetector.objects(name=searched_name).first().conditions.filter(iov=searched_iov).first()
