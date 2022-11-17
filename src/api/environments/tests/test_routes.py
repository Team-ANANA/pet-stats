import pytest

from api import app  # type: ignore

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_base_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is the root directory.' in response.data

def test_pie_graph_invalid_category(client):
    response = client.post('/V0/graph/pie', json={
        "type":"abc",
        "age":"123",
        "country":"canada",
        "category":"1123332"
    })
    
    assert response.status_code == 400

def test_pie_graph_no_category(client):
    response = client.post('/V0/graph/pie', json={
        "type":"abc",
        "age":"123",
        "country":"canada"
    })
    
    assert response.status_code == 400

def test_pie_graph_no_json(client):
    response = client.post('/V0/graph/pie')
    
    assert response.status_code == 400

def test_pie_graph_no_date_begin(client):
    response = client.post('/V0/graph/pie', json={
        "type":"abc",
        "age":"123",
        "country":"canada",
        "category":"type",
        "dateEnd":"1111/11/11"
    })
    
    assert response.status_code == 400

def test_pie_graph_no_date_end(client):
    response = client.post('/V0/graph/pie', json={
        "type":"abc",
        "age":"123",
        "country":"canada",
        "category":"type",
        "dateBegin":"1111/11/11"
    })
    
    assert response.status_code == 400