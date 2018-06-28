"""@package tue_conditionsDb
Test the cdb CLI
"""

import json
import unittest

from cdb_cli import CLI


class TestCdbService(unittest.TestCase):

    def setUp(self):
        self.cdb_cli = CLI()

    def test_list_subdetectors(self):
        response = self.cdb_cli.run('-ls')
        json_data = json.loads(response.to_json())
        self.assertTrue(len(json_data) >= 1)

    def test_show_subdetector(self):
        response = self.cdb_cli.run('-ss', 'Muon')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Muon')

    def test_show_condition(self):
        response = self.cdb_cli.run('-ss', 'Muon', '-sc', 'Gain')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Gain')

    #     def test_show_iov(self):
    #         response = self.service.run('-ss', 'Muon', '-si', '2018,06,21,17,26,38,437536')
    #         json_data = json.loads(response.to_json())
    #         self.assertEqual(json_data["iov"], '2018,06,21,17,26,38,437536')

    #     def test_show_iov_range(self):
    #         response = self.service.run('-ss', 'Muon', '-si', '2018,06,21,17,26,38,437536-2018,06,21,17,26,38,442798')
    #         self.assertEqual(len(response), 3)

    def test_list_subdetectors_conflict_ss(self):
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-ls', '-ss', 'Muon')

    def test_list_subdetectors_conflict_sc(self):
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-ls', '-ss', 'Muon', '-sc', 'Gain')

    def test_show_condition_without_sd(self):
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-sc', 'Gain')

    def test_show_iov_without_sd(self):
        with self.assertRaises(BaseException):
            self.cdb_cli.run('-si', '1529542553180')
