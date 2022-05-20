import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    URL = "http://learner:9007/"

    def test_test(self):
        user = {'user': 'charl'}
        resp = requests.get(self.URL, params=user)
        self.assertEquals(resp.status_code, 200)
        ob = {'user': 'charl'}
        self.assertEquals(resp.json(), ob)

    def test_api_predict(self):
        URL = self.URL + 'predict'
        # do python, java and kotlin work?
        params = {'code_to_format': 'cHVibGljIE1haW4oaW50IHkpIHsKICAgIHggPSB5OwogIH0K', 'language': 'java'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        params = {'code_to_format': 'cHVibGljIE1haW4oaW50IHkpIHsKICAgIHggPSB5OwogIH0K', 'language': 'python'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        params = {'code_to_format': 'cHVibGljIE1haW4oaW50IHkpIHsKICAgIHggPSB5OwogIH0K', 'language': 'kotlin'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        # error when language that does not exist yet?
        params = {'code_to_format': 'cHVibGljIE1haW4oaW50IHkpIHsKICAgIHggPSB5OwogIH0K', 'language': 'golang'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 500)

        # can handle no code?
        params = {'code_to_format': '', 'language': 'python'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        # can handle just nonsense in code?
        params = {'code_to_format': 'this is unformatted code', 'language': 'python'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 500)

    def test_api_finetune(self):
        URL = self.URL + 'finetune'
        # the same tests but for finetune
        params = {'language': 'java'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        params = {'language': 'python'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        params = {'language': 'kotlin'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 200)

        # error when language that does not exist yet?
        params = {'language': 'golang'}
        resp = requests.post(URL, data=params)
        self.assertEquals(resp.status_code, 500)


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main(exit=True)
