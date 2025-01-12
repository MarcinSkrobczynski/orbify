from fastapi import status


def test_get_health_returns_200_when_ok(endpoint_uri, client):
    response = client.get(endpoint_uri("health"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
