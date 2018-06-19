import unittest

from api import *

subdetector_1 = Subdetector(name='subdetector_test_1')
subdetector_2 = Subdetector(name='subdetector_test_2')
subdetector_3 = Subdetector(name='subdetector_test_3')


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        # TODO use the correct method to add the information on database instead of add manually....
        subdetector_1.save()
        subdetector_2.save()
        subdetector_3.save()

    @classmethod
    def tearDownClass(cls):
        # db = connect(test_db_name)
        # db.drop_database(test_db_name)
        subdetector_1.delete()
        subdetector_2.delete()
        subdetector_3.delete()

    """
        Method that evaluate if the list subdetector method is returning a collection of subdetectors.

        This test do not verify the conten of the returned list
    """

    def test_list_subdetectors(self):
        subdetectors = list_subdetectors()
        self.assertGreaterEqual(subdetectors.__len__(), 3)

    def test_show_subdetector(self):
        subdetector = show_subdetector(subdetector_1.name)
        self.assertIsNotNone(subdetector)
        self.assertEqual(subdetector.name, subdetector_1.name)

    def test_show_subdetector_not_found(self):
        subdetector = show_subdetector('invalid_subdetector')
        self.assertIsNone(subdetector)
