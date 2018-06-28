"""@package tue_conditionsDb
ConditionsDB API
"""
from datetime import datetime

from mongoengine import ComplexDateTimeField, FieldDoesNotExist

from classes.db_connect import DbConnect
from models import Subdetector, GlobalTag


class API(object):
    """
    TODO: Document it
    """
    ##
    # @var DATETIME_FORMAT
    # Masked used to format datetime
    DATETIME_FORMAT = '%Y,%m,%d,%H,%M,%S,%f'

    def __init__(self):
        DbConnect.get_connection('conditionsDB')

    @staticmethod
    def convert_date(date):
        """
        TODO: Document it
        """
        if isinstance(date, datetime):
            return ComplexDateTimeField()._convert_from_datetime(date)
        elif isinstance(date, str):
            return ComplexDateTimeField()._convert_from_string(date)
        return None

    @staticmethod
    def list_subdetectors():
        """
        function list_subdetectors() fetches a list of names of the subdetectors in the database from Subdetector
        collection

        python [file_name] -ls
        """
        return Subdetector.objects.values_list('name')

    @staticmethod
    def get_all_subdetectors():
        """
        function get_all_subdetectors() fetches all the subdetectors in the database from Subdetector collection

        python [file_name] -ls
        """
        return Subdetector.objects().all()

    @staticmethod
    def show_subdetector(searched_name):
        """
        function show_subdetector() fetches all the data i.e. name, conditions, etc
        related to the subdetector name, which User has requested for

        python [file_name] -ss
        """
        return Subdetector.objects(name=searched_name).first()

    @staticmethod
    def show_subdetector_conditions(searched_name):
        """
        function show_subdetector_conditions() fetches only the conditions
        related to the subdetector name, which User has requested for

        python [file_name] -ss "subdetector_name"
        """
        return API.show_subdetector(searched_name).conditions

    @staticmethod
    def show_subdetector_condition(searched_name, searched_condition):
        """
        function show_subdetector_condition() fetches all the data i.e. name, conditions, etc
        related to the subdetector name and conditions name, which User has requested for

        python [file_name] -ss "subdetector_name" -sc "condition_name"
        """
        return API.show_subdetector_conditions(searched_name).filter(name=searched_condition).first()

    @staticmethod
    def show_subdetector_tag(subdetector_name, searched_tag):
        """
        function show_subdetector_tag() fetches all the conditions that has a tag
        mentioned as an input by the user.

        python [file_name] -ss "subdetector_name" -st "tag_name"
        """
        if subdetector_name is not None and searched_tag is not None:
            return API.show_subdetector_conditions(subdetector_name).filter(tag=searched_tag).first()

        for s in API.get_all_subdetectors():
            for c in s.conditions:
                current_tag = c["tag"]

                if searched_tag == current_tag:
                    return c
        return None

    @staticmethod
    def show_subdetector_iov(searched_name, searched_iov):
        """
        function show_subdetector_iov() fetches all the conditions that has an IOV
        mentioned as an input by the user. OR a user can also look between the range of
        IOVs with two datetime's seperated by '-'

        python [file_name] -ss "subdetector_name" -si "datetime"
        python [file_name] -ss "subdetector_name" -si "datetime_from-datetime_to"
        """
        conditions = API.show_subdetector_conditions(searched_name)

        if "-" not in searched_iov:

            for c in conditions:

                current_iov_datetime = API.convert_date(c["iov"])

                formatted_searched_iov = API.convert_date(searched_iov)

                formatted_current_iov = datetime.strptime(current_iov_datetime, API.DATETIME_FORMAT)

                if formatted_current_iov == formatted_searched_iov:
                    return c
            return None

        found_conditions = []

        start, end = searched_iov.split("-")

        start_iov = API.convert_date(start)

        end_iov = API.convert_date(end)

        for c in conditions:

            current_iov_datetime = API.convert_date(c["iov"])

            current_formatted_iov = datetime.strptime(current_iov_datetime, API.DATETIME_FORMAT)

            if start_iov <= current_formatted_iov <= end_iov:
                found_conditions.append(c)

        return found_conditions

    @staticmethod
    def get_snapshot(searched_date_string, gt_name):
        """
        function show_subdetector_snapshot() fetches all the conditions that are for the
        datetime provided by the user. It checks between since and until dates of the condition

        python [file_name] -gs "searched_date_string" [-gt "global_tag_name"]
        """
        found_snapshot = []
        if searched_date_string in (None, ''):
            return found_snapshot

        if gt_name is not None:
            if not GlobalTag.objects(name=gt_name):
                GlobalTag(name=gt_name).save()

        for s in API.get_all_subdetectors():
            for c in s.conditions:
                since_date = API.convert_date(c["since"])
                until_date = API.convert_date(c["until"])
                formatted_since_date = datetime.strptime(since_date, API.DATETIME_FORMAT)
                formatted_until_date = datetime.strptime(until_date, API.DATETIME_FORMAT)
                formatted_searched_date = API.convert_date(searched_date_string)

                if formatted_since_date <= formatted_searched_date <= formatted_until_date:

                    found_snapshot.append(c)

                    if gt_name is not None:
                        prev_gt = c["global_tag"] if c["global_tag"] is not None else ""
                        if prev_gt == "":
                            c.global_tag = gt_name + ","
                        else:
                            c.global_tag = prev_gt + "," + gt_name

                        if gt_name + ',' not in prev_gt:
                            c.save()

        return found_snapshot

    @staticmethod
    def list_global_tags():
        """
        function list_globaltags() fetches a list of names of the Global Tags in the database from GlobalTag
        collection

        python [file_name] -lgt
        """
        return GlobalTag.objects.values_list('name')

    @staticmethod
    def get_data_global_tag(global_tag_name):
        """
        function get_data_global_tag() fetches all the conditions that are for the
        tag name provided by the user.

        python [file_name] -gtc "global_tag_name"
        """
        found_conditions = []

        for s in API.get_all_subdetectors():
            for c in s.conditions:
                global_tag = c["global_tag"] if c["global_tag"] is not None else ""

                if global_tag_name + ',' in global_tag:
                    found_conditions.append(c)

        return found_conditions

    @staticmethod
    def add_subdetector(new_subdetector):
        """
        function add_subdetector() adds a new subdetector or a json file mentioned by the user

        python [file_name] -as "subdetector_name"
        """
        try:
            Subdetector(**new_subdetector).save()
        except FieldDoesNotExist:
            return -1
        except TypeError:
            return -2
        return 1
