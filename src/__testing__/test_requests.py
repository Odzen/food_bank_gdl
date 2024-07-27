from src.main import testing_client
from src.config.jwt import get_settings as jwt_settings

def test_request_create_auth():

    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    
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

    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    
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
    
    
def list_all_requests():

    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    
    response = testing_client.get(
        "/requests/",
        headers=headers
    )
    
    assert response.status_code == 200
    
def test_request_by_id():
    # Bearer token in header
    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    response = testing_client.get(
        "/requests/6531e76fc7e8b449103d6afb",
        headers=headers  # Pasar los encabezados como un diccionario
    )
    
    assert response.status_code == 404