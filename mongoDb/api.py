"""@package mongoDb
ConditionsDB API
"""
from datetime import datetime

from mongoengine import ComplexDateTimeField

from classes.db_connect import DbConnect
from models import Subdetector


class API(object):

    def __init__(self):
        DbConnect.get_connection('conditionsDB')

    @staticmethod
    def convert_date(date):
        if isinstance(date, datetime):
            return ComplexDateTimeField()._convert_from_datetime(date)
        elif isinstance(date, str):
            return ComplexDateTimeField()._convert_from_string(date)
        return None

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
    def show_subdetector_tag(searched_name, searched_tag):

        if searched_name is not None:
            return API.show_subdetector_conditions(searched_name).filter(tag=searched_tag)

        subdetectors = Subdetector.objects.all()
        found_tag = []

        for s in subdetectors:
            for c in s.conditions:
                current_tag = c["tag"]

                if searched_tag == current_tag:
                    found_tag.append(c)

        return found_tag

    @staticmethod
    def show_subdetector_iov(searched_name, searched_iov):

        conditions = API.show_subdetector(searched_name).conditions

        if "-" not in searched_iov:

            for c in conditions:

                current_iov_datetime = API.convert_date(c["iov"])

                formatted_searched_iov = API.convert_date(searched_iov)

                formatted_current_iov = datetime.strptime(current_iov_datetime, '%Y,%m,%d,%H,%M,%S,%f')

                if formatted_current_iov == formatted_searched_iov:
                    return c
            return None

        found_conditions = []

        start, end = searched_iov.split("-")

        start_iov = API.convert_date(start)

        end_iov = API.convert_date(end)

        for c in conditions:

            current_iov_datetime = API.convert_date(c["iov"])

            current_formatted_iov = datetime.strptime(current_iov_datetime, '%Y,%m,%d,%H,%M,%S,%f')

            if (current_formatted_iov >= start_iov and current_formatted_iov <= end_iov):
                found_conditions.append(c)

        return found_conditions

    @staticmethod
    def show_subdetector_snapshot(searched_date):

        subdetectors = Subdetector.objects.all()
        found_snapshot = []

        for s in subdetectors:
            for c in s.conditions:
                since_date = API.convert_date(c["since"])
                until_date = API.convert_date(c["until"])
                formatted_since_date = datetime.strptime(since_date, '%Y,%m,%d,%H,%M,%S,%f')
                formatted_until_date = datetime.strptime(until_date, '%Y,%m,%d,%H,%M,%S,%f')
                formatted_searched_date = API.convert_date(searched_date)

                if (formatted_searched_date >= formatted_since_date and formatted_searched_date <= formatted_until_date):
                    found_snapshot.append(c)

        return found_snapshot

    @staticmethod
    def add_subdetector(new_subdetector):
        try:
            Subdetector(**new_subdetector).save()
        except ValueError:
            return -1

        return 1
