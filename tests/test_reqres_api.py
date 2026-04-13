from api.reqres_api import ReqResAPI

def test_create_and_verify_user():
    api = ReqResAPI()

    # Create User
    response = api.create_user(name="Neo", job="QA")
    assert response.status_code == 201

    response_body = response.json()
    assert response_body["name"] == "Neo"
    assert response_body["job"] == "QA"
    assert "id" in response_body

    # Verify user exists (best possible validation for ReqRes)
    users_response = api.get_users(page=1)
    assert users_response.status_code == 200

    users = users_response.json()["data"]
    assert isinstance(users, list)