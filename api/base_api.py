import requests

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, payload):
        return requests.post(
            url=f"{self.base_url}{endpoint}",
            json=payload
        )

    def get(self, endpoint):
        return requests.get(
            url=f"{self.base_url}{endpoint}"
        )