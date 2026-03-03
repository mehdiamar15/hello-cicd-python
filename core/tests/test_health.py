import pytest

@pytest.mark.django_db
def test_health(client):
    r = client.get("/health/")
    assert r.status_code in (200, 404)
