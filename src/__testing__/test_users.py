from src.main import testing_client
from src.config.jwt import jwt_settings

def test_users():
    # Bearer token in header
    headers = {"Authorization": f"Bearer {jwt_settings.jwt_admin_token}"}
    response = testing_client.get(
        "/users/",
        headers=headers  # Pasar los encabezados como un diccionario
    )
    
    assert response.status_code == 200
    
    
def test_users_by_id():
    # Bearer token in header
    headers = {"Authorization": f"Bearer {jwt_settings.jwt_admin_token}"}
    response = testing_client.get(
        "/users/1",
        headers=headers  # Pasar los encabezados como un diccionario
    )
    
    assert response.status_code == 401
    
def test_users_create():

    headers = {"Authorization": f"Bearer {jwt_settings.jwt_admin_token}"}
    
    json={
        "first_name": "employee",
        "last_name": "employee",
        "email": "juan@mail.com",
        "role": "admin",
        "password": "password",
        "identification": "14526"
    }
    
    response = testing_client.post(
        "/users/",
        headers=headers,
        json=json
    )
    
    assert "approved" in response.json()["detail"]
    
    assert response.status_code == 409