import json
import os
import unittest

from app import app

class ProductionPlanTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        with open(os.path.join(test_data_dir, 'test_correct_payload.json')) as f:
            self.test_correct_payload = json.load(f)
            f.close()
        with open(os.path.join(test_data_dir, 'test_error_payload.json')) as f:
            self.test_error_payload = json.load(f)
            f.close()


    def test_dispatch_correct_response(self):
        expected_response = [
            {"name": "windpark1", "p": 90.0},
            {"name": "windpark2", "p": 21.6},
            {"name": "gasfiredbig1", "p": 460.0},
            {"name": "gasfiredbig2", "p": 338.4},
            {"name": "gasfiredsomewhatsmaller", "p": 0.0},
            {"name": "tj1", "p": 0.0}
        ]

        response = self.app.post('/api/v1/productionplan', data=json.dumps(self.test_correct_payload),
                                 content_type='application/json')

        self.assertEqual(200, response.status_code)

        data = json.loads(response.data)

        self.assertEqual(data, expected_response)


    def test_dispatch_error_response(self):
        response = self.app.post('/api/v1/productionplan', data=json.dumps(self.test_error_payload),
                                 content_type='application/json')

        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
