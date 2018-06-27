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

    '''
    function list_subdetectors() fetches all the subdetectors in the database from Subdetector colection 
    
    python [file_name] -ls
    '''

    @staticmethod
    def list_subdetectors():
        return Subdetector.objects.values_list('name')

    @staticmethod
    def get_all_subdetectors():
        return Subdetector.objects()

    '''
    function show_subdetector() fetches all the data i.e. name, conditions, etc 
    related to the subdetector name, which User has requested for
    
    python [file_name] -ss   
    '''
    @staticmethod
    def show_subdetector(searched_name):
        return Subdetector.objects(name=searched_name).first()


    '''
    function show_subdetector_conditions() fetches only the conditions 
    related to the subdetector name, which User has requested for
    
    python [file_name] -ss [subdetector_name]   
    '''
    @staticmethod
    def show_subdetector_conditions(searched_name):
        return API.show_subdetector(searched_name).conditions


    '''
    function show_subdetector_condition() fetches all the data i.e. name, conditions, etc
    related to the subdetector name and conditions name, which User has requested for
    
    python [file_name] -ss [subdetector_name] -sc [condition_name]   
    '''
    @staticmethod
    def show_subdetector_condition(searched_name, searched_condition):
        return API.show_subdetector_conditions(searched_name).filter(name=searched_condition).first()

    '''
    function show_subdetector_tag() fetches all the conditions that has a tag 
    mentioned as an inut by the user.

    python [file_name] -ss [subdetector_name] -st [tag_name]   
    '''
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


    '''
    function show_subdetector_iov() fetches all the conditions that has an IOV 
    mentioned as an input by the user. OR a user can also look between the range of
    IOVs with two datetime's seperated by '-'

    python [file_name] -ss [subdetector_name] -si [iov]   
    python [file_name] -ss [subdetector_name] -si [iov-iov]
    '''
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


    '''
    function show_subdetector_snapshot() fetches all the conditions that are for the
    datetime provided by the user. It checks between since and until dates of the condition

    python [file_name] -ss [subdetector_name] -sn [iov]
    '''
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


    '''
    function add_subdetector() adds a new subdetector or a json file mentioned by the user

    python [file_name] -as [subdetector_name]
    '''
    @staticmethod
    def add_subdetector(new_subdetector):
        try:
            Subdetector(**new_subdetector).save()
        except ValueError:
            return -1

        return 1
