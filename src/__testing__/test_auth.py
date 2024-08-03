from src.main import testing_client
from src.config.jwt import get_settings as jwt_settings

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
    assert response.status_code == 404
    assert "doesn't exist" in response.json()["detail"]
    
def test_read_login():
    response = testing_client.post(
        "/login/",
        data = {
            "grant_type": "password",
            "username": "juan@mail.com",
            "password": "password",
            "scope": "",
            "client_id": "string",
            "client_secret": "string"
        },
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"
        },
    )    
    
    assert response.status_code == 200
    
def test_me():
    # Bearer token in header
    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    response = testing_client.get(
        "/me/",
        headers=headers  # Pasar los encabezados como un diccionario
    )
    
    assert response.status_code == 200