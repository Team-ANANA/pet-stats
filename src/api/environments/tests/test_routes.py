import pytest
import json
from unittest.mock import patch
from api import app


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
        "type": "abc",
        "age": "123",
        "country": "canada",
        "category": "1123332"
    })

    assert response.status_code == 400


def test_pie_graph_no_category(client):
    response = client.post('/V0/graph/pie', json={
        "type": "abc",
        "age": "123",
        "country": "canada"
    })

    assert response.status_code == 400


def test_pie_graph_no_json(client):
    response = client.post('/V0/graph/pie')

    assert response.status_code == 400


def test_pie_graph_no_date_begin(client):
    response = client.post('/V0/graph/pie', json={
        "type": "abc",
        "age": "123",
        "country": "canada",
        "category": "type",
        "dateEnd": "1111/11/11"
    })

    assert response.status_code == 400


def test_pie_graph_no_date_end(client):
    response = client.post('/V0/graph/pie', json={
        "type": "abc",
        "age": "123",
        "country": "canada",
        "category": "type",
        "dateBegin": "1111/11/11"
    })

    assert response.status_code == 400

# hardcoded method to mock db response based on sql query
def mock_execute_get_entry_sql(sql):
    if sql == "SELECT * FROM type;":
        return [(1, 'dog'), (2, 'cat'), (3, 'other')]
    elif sql == "SELECT * FROM age;":
        return [(1, 'baby'), (2, 'young'), (3, 'adult')]
    elif sql == "SELECT * FROM breed;":
        return [(1, 1, 'affenpinscher'), (2, 1, 'Afghan Hound'), (3, 2, 'American Curl'), (4, 3, 'Alpaca')]
    elif sql == "SELECT * FROM gender;":
        return [(1, 'male'), (2, 'female'), (3, 'asexual')]
    elif sql == "SELECT * FROM size;":
        return [(1, 'small'), (2, 'medium'), (3, 'large'), (4, 'extra large')]
    elif sql == "SELECT * FROM status;":
        return [(1, 'adaptable'), (2, 'adapted'), (3, 'hold')]
    elif sql == "SELECT * FROM country;":
        return [(1, 'CA'), (2, 'US'), (3, 'MX')]
    elif sql == "SELECT * FROM province;":
        return [(1, 1, 'AB'), (2, 1, 'BC'), (3, 1, 'MB'), (4, 1, 'NB'),
                (5, 1, 'NL'), (6, 1, 'NS'), (7, 1,
                                             'ON'), (8, 2, 'AL'), (9, 2, 'AK'),
                (10, 2, 'AZ'), (11, 3, 'AGS'), (12, 3, 'BCN'), (13, 3, 'BCS')]
    else:
        return []

# use the mocked execute sql function to mock rows returned from db
@patch('sql_util.execute_sql', mock_execute_get_entry_sql)
def test_get_entries(client):
    response = client.get('/V0/data/entry/')
    data = json.loads(response.data)
    assert data['type'] == {'dog': 1, 'cat': 2, 'other': 3}
    assert data['age'] == {'baby': 1, 'young': 2, 'adult': 3}
    assert data['breed'] == {'dog': {'affenpinscher': 1, 'Afghan Hound': 2}, 'cat': {
        'American Curl': 3}, 'other': {'Alpaca': 4}}
    assert data['gender'] == {'male': 1, 'female': 2, 'asexual': 3}
    assert data['size'] == {'small': 1,
                            'medium': 2, 'large': 3, 'extra large': 4}
    assert data['status'] == {'adaptable': 1, 'adapted': 2, 'hold': 3}
    assert data['country'] == {'CA': 1, 'US': 2, 'MX': 3}
    assert data['province'] == {'CA': {'AB': 1, 'BC': 2, 'MB': 3, 'NB': 4, 'NL': 5, 'NS': 6, 'ON': 7}, 'US': {
        'AL': 8, 'AK': 9, 'AZ': 10}, 'MX': {'AGS': 11, 'BCN': 12, 'BCS': 13}}
    assert response.status_code == 200

def test_get_pie_graph(client):
    with patch('sql_util.execute_sql') as mock_sql:
        mock_sql.return_value = [(12, 'small'), (10, 'large'), (5, 'medium')]
        response = client.post('/V0/graph/pie', json={
            "type": ['abc'],
            "age": [123],
            "country": ["canada"],
            "category": "size",
            "dateBegin": "2022-11-11",
            "dateEnd": "2022-11-22"
        })
        sql = mock_sql.call_args.args[0]
        sql = str.lower(sql)
        assert "type in (select * from @type)" in sql
        assert "age in (select * from @age)" in sql
        assert "country in (select * from @country)" in sql
        assert "group by size" in sql
        assert "published_at >= 2022-11-11 00:00:00" in sql
        assert "published_at <= 2022-11-22 00:00:00" in sql
        assert json.loads(response.data) == {'small': 12, 'large':10, 'medium':5}
