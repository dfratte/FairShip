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
# @var CONDITION_3
# Dummy condition for subdetector 1, with the same tag as CONDITION_2
# TODO Add documentation for parameters
API = API()

SOURCE_1 = Source(name='Source_test_1')

SUBDETECTOR_1 = Subdetector(name='subdetector_test_1')
SUBDETECTOR_2 = Subdetector(name='subdetector_test_2')

CONDITION_1 = Condition(name='condition_test_1', iov=datetime.now(), tag='tag_test_1')
PARAMETER_1 = Parameter(name='parameter_test_1', iov=datetime.now(), value='parameter_value_test_1')
CONDITION_2 = Condition(name='condition_test_2', iov=datetime.now(), tag='tag_test_2')
CONDITION_3 = Condition(name='condition_test_3', iov=datetime.now(), tag='tag_test_3')
PARAMETER_2 = Parameter(name='parameter_test_2', iov=datetime.now(), value='parameter_value_test_2')
PARAMETER_3 = Parameter(name='parameter_test_3', iov=datetime.now(), value='parameter_value_test_3')

SUBDETECTOR_3 = Subdetector()


class TestApi(unittest.TestCase):
    """
    Unit tests for API class
    """

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        SOURCE_1.save()
        CONDITION_1.parameters.append(PARAMETER_1)
        CONDITION_2.parameters.append(PARAMETER_2)
        CONDITION_3.parameters.append(PARAMETER_3)
        CONDITION_1.source = SOURCE_1
        CONDITION_2.source = SOURCE_1
        SUBDETECTOR_1.conditions.append(CONDITION_1)
        SUBDETECTOR_1.conditions.append(CONDITION_2)
        SUBDETECTOR_1.conditions.append(CONDITION_3)
        SUBDETECTOR_3 = SUBDETECTOR_1
        SUBDETECTOR_1.save()
        SUBDETECTOR_2.save()

    @classmethod
    def tearDownClass(cls):
        SUBDETECTOR_1.delete()
        SUBDETECTOR_2.delete()

    def test_list_subdetectors(self):
        """
        Method to evaluate if the list subdetector method is returning a list of subdetector names.
        """
        subdetectors = API.list_subdetectors()
        self.assertGreaterEqual(subdetectors.count, 2)
        self.assertTrue(isinstance(subdetectors[1], unicode))

    def test_get_all_subdetectors(self):
        """
        Method to evaluate if the list subdetector method is returning a list of subdetectors.
        This test does not verify the content of the returned list.
        """
        subdetectors = API.get_all_subdetectors()
        self.assertGreaterEqual(subdetectors.count(), 2)
        self.assertIsNotNone(subdetectors[0].conditions)
        self.assertIsNotNone(subdetectors[0].conditions[0].name)
        self.assertIsNotNone(subdetectors[0].conditions[0].parameters)
        self.assertIsNotNone(subdetectors[0].conditions[0].parameters[0].name)

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
        self.assertEqual(conditions.count(), SUBDETECTOR_1.conditions.count())

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

    def test_show_subdetector_tag(self):
        condition = API.show_subdetector_tag(SUBDETECTOR_1.name, None)
        self.assertIsNone(condition)
        condition = API.show_subdetector_tag(None, CONDITION_3.tag)
        self.assertEqual(condition.name, CONDITION_3.name)
        condition = API.show_subdetector_tag(None, None)
        self.assertIsNone(condition)
        condition = API.show_subdetector_tag(SUBDETECTOR_1.name, CONDITION_3.tag)
        self.assertEqual(condition.name, CONDITION_3.name)

    def test_show_subdetector_iov(self):
        # TODO implement it
        pass

    def test_show_subdetector_with_invalid_condition(self):
        """
        Search subdetector by invalid condition name.
        """
        condition = API.show_subdetector_condition(SUBDETECTOR_1.name, 'invalid_condition')
        self.assertIsNone(condition)

    def test_add_subdetector(self):
        """
        Add a subdetector to the database from json file.

        Try to add an invalid loaded json into the database, which should raise a FieldDoesNotExist exception

        Try to add an invalid json (in this case an empty string) into the database, which should raise a
        TypeError exception
        """
        self.assertEqual(API.add_subdetector(json.loads(SUBDETECTOR_3.to_json())), 1)
        self.assertEqual(-1, API.add_subdetector(json.loads('{"InvalidField":"InvalidValue"}')))
        self.assertEqual(-2, API.add_subdetector(''))

    def test_convert_date(self):
        """
        Test the convert date function
        """
        date = datetime.now()
        self.assertEqual(API.convert_date(date), date.strftime(API.DATETIME_FORMAT))
        self.assertEqual(API.convert_date(date.strftime(API.DATETIME_FORMAT)), date)
        self.assertEqual(API.convert_date(1), None)
