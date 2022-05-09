import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000/"

    def test_test(self):
        user = {'user': 'charl'}
        resp = requests.get(self.URL, params=user)
        self.assertEquals(resp.status_code, 200)
        ob = {'user': 'charl'}
        self.assertEquals(resp.json(), ob)