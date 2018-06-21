import unittest
import json
from cdb_service import Service

class TestCdbService(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    def test_list_subdetectors(self):
        response = self.service.run('-ls')
        json_data = json.loads(response.to_json())
        self.assertTrue(len(json_data) >= 1)

    def test_show_subdetector(self):
        response = self.service.run('-ss', 'Muon')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Muon')

    def test_show_condition(self):
        response = self.service.run('-ss', 'Muon', '-sc', 'Gain')
        json_data = json.loads(response.to_json())
        self.assertEqual(json_data["name"], 'Gain')

    def test_list_subdetectors_conflict_ss(self):
        with self.assertRaises(BaseException):
            self.service.run('-ls', '-ss', 'Muon')
 
    def test_list_subdetectors_conflict_sc(self):
        with self.assertRaises(BaseException):
            self.service.run('-ls', '-ss', 'Muon', '-sc', 'Gain')

    def test_show_condition_without_sd(self):
        with self.assertRaises(BaseException):
            self.service.run('-sc', 'Gain')

    def test_show_iov_without_sd(self):
        with self.assertRaises(BaseException):
            self.service.run('-si', '1529542553180')

if __name__ == '__main__':
    unittest.main()
