"""@package docstring
Unittest developed to guarantee the api integrity
"""
import json
import unittest
from datetime import datetime

from api import API
from models import Condition, Parameter, Source, Subdetector

##
# @var API
# Instance of API class to be tested
# @var SUBDETECTOR_1
# Dummy subdetector 1 with 2 conditions
# @var SUBDETECTOR_2
# Dummy subdetector 2 without any conditions
# @var CONDITION_1
# Dummy condition for subdetector 1
# @var CONDITION_2
# Dummy condition for subdetector 1
API = API()

SOURCE_1 = Source(name='Source_test_1')

SUBDETECTOR_1 = Subdetector(name='subdetector_test_1')
SUBDETECTOR_2 = Subdetector(name='subdetector_test_2')

CONDITION_1 = Condition(name='condition_test_1', iov=datetime.now(), tag='tag_test_1')
PARAMETER_1 = Parameter(name='parameter_test_1', iov=datetime.now(), value='parameter_value_test_1')
CONDITION_2 = Condition(name='condition_test_2', iov=datetime.now(), tag='tag_test_2')
PARAMETER_2 = Parameter(name='parameter_test_2', iov=datetime.now(), value='parameter_value_test_2')

SUBDETECTOR_3 = Subdetector()


class TestApi(unittest.TestCase):
    """
    Unit tests for API class
    """

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        # TODO use the correct method to add the information on database instead of add manually....
        SOURCE_1.save()
        CONDITION_1.parameters.append(PARAMETER_1)
        CONDITION_2.parameters.append(PARAMETER_2)
        CONDITION_1.source = SOURCE_1
        CONDITION_2.source = SOURCE_1
        SUBDETECTOR_1.conditions.append(CONDITION_1)
        SUBDETECTOR_1.conditions.append(CONDITION_2)
        SUBDETECTOR_3 = SUBDETECTOR_1
        SUBDETECTOR_1.save()
        SUBDETECTOR_2.save()

    @classmethod
    def tearDownClass(cls):
        SUBDETECTOR_1.delete()
        SUBDETECTOR_2.delete()

    def test_list_subdetectors(self):
        """Method to evaluate if the list subdetector method is returning a collection of subdetectors.

        This test does not verify the content of the returned list.
        """
        subdetectors = API.list_subdetectors()
        self.assertGreaterEqual(subdetectors.count(), 2)

    def test_show_subdetector(self):
        """
        Retrieve an existing subdetector.
        """
        subdetector = API.show_subdetector(SUBDETECTOR_1.name)
        self.assertEqual(subdetector.name, SUBDETECTOR_1.name)

    def test_show_subdetector_not_found(self):
        """
        Try to retrieve a subdetector that does not exist in the DB.
        """
        subdetector = API.show_subdetector('invalid_subdetector')
        self.assertIsNone(subdetector)

    def test_show_subdetector_conditions(self):
        """
        Retrieve subdetector that has 2 conditions.
        """
        conditions = API.show_subdetector_conditions(SUBDETECTOR_1.name)
        self.assertEqual(conditions.count(), 2)

    def test_show_subdetector_without_conditions(self):
        """
        Retrieve a subdetector that does not contain any condition.
        """
        conditions = API.show_subdetector_conditions(SUBDETECTOR_2.name)
        self.assertEqual(conditions.count(), 0)

    def test_show_subdetector_condition(self):
        """
        Find subdetector by valid condition name.
        """
        condition = API.show_subdetector_condition(SUBDETECTOR_1.name, CONDITION_1.name)
        self.assertEqual(condition.name, CONDITION_1.name)

    def test_show_subdetector_with_invalid_condition(self):
        """
        Search subdetector by invalid condition name.
        """
        condition = API.show_subdetector_condition(SUBDETECTOR_1.name, 'invalid_condition')
        self.assertIsNone(condition)

    def test_add_subdetector(self):
        """
        Add a subdetector to the database from json file.
        """
        self.assertEqual(API.add_subdetector(json.loads(SUBDETECTOR_3.to_json())), 1)
