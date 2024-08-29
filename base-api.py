import requests
from utils.config_reader import ConfigReader

class BaseAPI:
    def __init__(self):
        config = ConfigReader()
        self.base_url = config.get_base_url()
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=data, json=json)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, data=data, json=json)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        return response
