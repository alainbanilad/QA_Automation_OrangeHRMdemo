import requests

class BaseAPI:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self._headers = headers or {}

    def post(self, endpoint, payload):
        return requests.post(
            url=f"{self.base_url}{endpoint}",
            json=payload,
            headers=self._headers
        )

    def get(self, endpoint):
        return requests.get(
            url=f"{self.base_url}{endpoint}",
            headers=self._headers
        )