"""@package mongoDb
ConditionsDB API
"""
from classes.db_connect import DbConnect
from models import Subdetector
from datetime import datetime
from mongoengine import ComplexDateTimeField

class API(object):

    def __init__(self):
        DbConnect.get_connection('conditionsDB')

    @staticmethod
    def convert_date(date):
        if type(date) is datetime:
            return ComplexDateTimeField()._convert_from_datetime(date)
        elif type(date) is str:
            return ComplexDateTimeField()._convert_from_string(date)

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
        return API.show_subdetector_conditions(searched_name).filter(name=searched_condition).first()

    @staticmethod
    def show_subdetector_iov(searched_name, searched_iov):

        conditions = API.show_subdetector(searched_name).conditions

        if "-" not in searched_iov:

            for c in conditions:

                current_iov_datetime = API.convert_date(c["iov"])

                formatted_searched_iov = API.convert_date(searched_iov)

                formatted_current_iov = datetime.strptime(current_iov_datetime,'%Y,%m,%d,%H,%M,%S,%f')

                if formatted_current_iov == formatted_searched_iov:

                    return c

        else:

            found_conditions = []

            start, end = searched_iov.split("-")

            start_iov = API.convert_date(start)

            end_iov = API.convert_date(end)

            for c in conditions:

                current_iov_datetime = API.convert_date(c["iov"])

                current_formatted_iov = datetime.strptime(current_iov_datetime, '%Y,%m,%d,%H,%M,%S,%f')

                if ( current_formatted_iov >= start_iov and current_formatted_iov <= end_iov):
                    
                    found_conditions.append(c)

            return found_conditions

    @staticmethod
    def add_subdetector(new_subdetector):
        try:
            Subdetector(**new_subdetector).save()
        except ValueError:
            return -1

        return 1
