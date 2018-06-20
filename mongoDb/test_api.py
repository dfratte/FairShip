"""@package docstring
Unittest developed to guarantee the api integrity
"""

import unittest

from api import API
from models import Subdetector

API = API()

SUBDETECTOR_1 = Subdetector(name='subdetector_test_1')
SUBDETECTOR_2 = Subdetector(name='subdetector_test_2')
SUBDETECTOR_3 = Subdetector(name='subdetector_test_3')


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        # TODO use the correct method to add the information on database instead of add manually....
        SUBDETECTOR_1.save()
        SUBDETECTOR_2.save()
        SUBDETECTOR_3.save()

    @classmethod
    def tearDownClass(cls):
        SUBDETECTOR_1.delete()
        SUBDETECTOR_2.delete()
        SUBDETECTOR_3.delete()

    def test_list_subdetectors(self):
        """Method that evaluate if the list subdetector method is returning a collection of subdetectors.

        This test do not verify the conten of the returned list
        """
        subdetectors = API.list_subdetectors()
        self.assertGreaterEqual(subdetectors.count(), 3)

    def test_show_subdetector(self):
        subdetector = API.show_subdetector(SUBDETECTOR_1.name)
        self.assertIsNotNone(subdetector)
        self.assertEqual(subdetector.name, SUBDETECTOR_1.name)

    def test_show_subdetector_not_found(self):
        subdetector = API.show_subdetector('invalid_subdetector')
        self.assertIsNone(subdetector)
