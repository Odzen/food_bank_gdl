from src.main import testing_client


def test_read_main():
    response = testing_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Welcome to Food Bank API, explore the docs at /docs."}