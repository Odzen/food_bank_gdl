from src.main import testing_client
from src.config.jwt import jwt_settings


def test_request_create_auth():

    headers = {"Authorization": f"Bearer {jwt_settings.jwt_admin_token}"}
    
    json={
        "email": "juan_velasquez@mail.com"
    }
    
    response = testing_client.post(
        "/requests/auth/",
        headers=headers,
        json=json
    )
    
    assert "pending" in response.json()["detail"]
    
    assert response.status_code == 409
    
def test_request_create():

    headers = {"Authorization": f"Bearer {jwt_settings.jwt_admin_token}"}
    
    json= {
        "title": "Desempacar platanos",
        "description": "Necesitamos aprobación para abrir una caja",
        "type": "authorization"
    }
    
    response = testing_client.post(
        "/requests/",
        headers=headers,
        json=json
    )
    
    assert response.status_code == 200