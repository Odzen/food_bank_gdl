from src.main import testing_client

def test_read_login_fail_schema():
    response = testing_client.post(
        "/login/",
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': 
            [
                {
                    'type': 'missing', 
                    'loc': ['body', 'username'],
                    'msg': 'Field required',
                    'input': None,
                    'url': 'https://errors.pydantic.dev/2.3/v/missing'
                 },
                {
                    'type': 'missing',
                    'loc': ['body', 'password'],
                    'msg': 'Field required',
                    'input': None,
                    'url': 'https://errors.pydantic.dev/2.3/v/missing'
                }
            ]
    }
    
def test_read_login_fail_format():
    response = testing_client.post(
        "/login/",
        json={"username": "mock", "password": "12546"},
    )
    assert response.status_code == 422
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]
    
def test_read_login_fail_credentials():
    response = testing_client.post(
        "/login/",
        json={"username": "juan@mail.com", "password": "12546"},
    )
    print(response.json())
    assert response.status_code == 422
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]