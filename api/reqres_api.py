from api.base_api import BaseAPI

class ReqResAPI(BaseAPI):
    def __init__(self):
        super().__init__("https://reqres.in")

    def create_user(self, name, job):
        payload = {
            "name": name,
            "job": job
        }
        return self.post("/api/users", payload)

    def get_users(self, page=1):
        return self.get(f"/api/users?page={page}")