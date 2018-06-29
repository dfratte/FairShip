"""@package tue_conditionsDb
Test the cdb CLI
"""

import json
import unittest

from cdb_cli import CLI


class TestCdbService(unittest.TestCase):
    """
    Used to execute automated unittests on the cdb_cli.py
    """

    def setUp(self):
        """
        Sets up the CLI client before the tests
        """
        self.cdb_cli = CLI()

    def test_list_subdetectors(self):
        """
        Method to evaluate if the list subdetector method is returning a list of subdetector names.
        """
        response = self.cdb_cli.run('-ls')
        json_data = json.loads(response.to_json())
        self.assertTrue(len(json_data) >= 1)

    def test_show_subdetector(self):
        """
        Retrieve an existing subdetector.
        """
        response = self.cdb_cli.run('-ss', 'Muon')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Muon')

    def test_show_condition(self):
        """
        Find subdetector by valid condition name.
        """
        response = self.cdb_cli.run('-ss', 'Muon', '-sc', 'Gain')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Gain')

    def test_list_subdetectors_conflict_ss(self):
        """
        Validates that the CLI throws exception if you try to use mutually exclusive flags (-ls and -ss)
        """
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-ls', '-ss', 'Muon')

    def test_list_subdetectors_conflict_sc(self):
        """
        Validates that the CLI throws exception if you try to use mutually exclusive flags (ls, -ss, -sc)
        """
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-ls', '-ss', 'Muon', '-sc', 'Gain')

    def test_show_condition_without_sd(self):
        """
        Validates that the CLI throws exception if you try to find a condition without providing
        the subdetector name.
        """
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-sc', 'Gain')

    def test_show_iov_without_sd(self):
        """
        Validates that the CLI throws exception if you try to find an IOV without providing
        the subdetector name.
        """
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-si', '1529542553180')
