from src.main import testing_client

from src.config.jwt import get_settings as jwt_settings

def test_ticket_create():

    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    
    json= {
        "title": "New ticket",
        "description": "description",
        "category": "categoria",
        "urgency": "medium"
    }
    
    response = testing_client.post(
        "/tickets/",
        headers=headers,
        json=json
    )
    
    assert response.status_code == 200
    
def list_all_tickets():

    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    
    response = testing_client.get(
        "/tickets/",
        headers=headers
    )
    
    assert response.status_code == 200
    
def test_ticket_by_id():
    # Bearer token in header
    headers = {"Authorization": f"Bearer {jwt_settings().jwt_admin_token}"}
    response = testing_client.get(
        "/test_tickes/6531e76fc7e8b449103d6afb",
        headers=headers  # Pasar los encabezados como un diccionario
    )
    
    assert response.status_code == 404