import pytest
from api import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_base_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is the root directory. Try out the /hello route!' in response.data

def test_hello_world(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data
