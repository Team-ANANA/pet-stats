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
    sql = sql.lower()
    if sql == "select * from type;":
        return [(1, 'dog'), (2, 'cat'), (3, 'other')]
    elif sql == "select * from age;":
        return [(1, 'baby'), (2, 'young'), (3, 'adult')]
    elif sql == "select * from breed;":
        return [(1, 1, 'affenpinscher'), (2, 1, 'Afghan Hound'), (3, 2, 'American Curl'), (4, 3, 'Alpaca')]
    elif sql == "select * from gender;":
        return [(1, 'male'), (2, 'female'), (3, 'asexual')]
    elif sql == "select * from size;":
        return [(1, 'small'), (2, 'medium'), (3, 'large'), (4, 'extra large')]
    elif sql == "select * from status;":
        return [(1, 'adaptable'), (2, 'adapted'), (3, 'hold')]
    elif sql == "select * from country;":
        return [(1, 'CA'), (2, 'US'), (3, 'MX')]
    elif sql == "select * from state;":
        return [(1, 1, 'AB'), (2, 1, 'BC'), (3, 1, 'MB'), (4, 1, 'NB'),
                (5, 1, 'NL'), (6, 1, 'NS'), (7, 1,'ON'), (8, 2, 'AL'), (9, 2, 'AK'),
                (10, 2, 'AZ'), (11, 3, 'AGS'), (12, 3, 'BCN'), (13, 3, 'BCS')]
    else:
        return []

# use the mocked execute sql function to mock rows returned from db
@patch('sql_util.execute_sql', mock_execute_get_entry_sql)
def test_get_entries(client):
    response = client.get('/V0/data/entry')
    data = json.loads(response.data)
    assert data['Type'] == {'dog': 1, 'cat': 2, 'other': 3}
    assert data['Age'] == {'baby': 1, 'young': 2, 'adult': 3}
    assert data['Breed'] == {'dog': {'affenpinscher': 1, 'Afghan Hound': 2}, 'cat': {
        'American Curl': 3}, 'other': {'Alpaca': 4}}
    assert data['Gender'] == {'Male': 2, 'Female': 1, 'Unknown': 3}
    assert data['Size'] == {'small': 1,
                            'medium': 2, 'large': 3, 'extra large': 4}
    assert data['Status'] == {'adaptable': 1, 'adapted': 2, 'hold': 3}
    assert data['Country'] == {'CA': 1, 'US': 2, 'MX': 3}
    assert data['State'] == {'CA': {'AB': 1, 'BC': 2, 'MB': 3, 'NB': 4, 'NL': 5, 'NS': 6, 'ON': 7}, 'US': {
        'AL': 8, 'AK': 9, 'AZ': 10}, 'MX': {'AGS': 11, 'BCN': 12, 'BCS': 13}}
    assert response.status_code == 200

def test_get_pie_graph(client):
    with patch('sql_util.execute_multiple_sql') as mock_sql:
        mock_sql.return_value = [(12, 'ON'), (10, 'SK'), (5, 'BC')]
        response = client.post('/V0/graph/pie', json= {
            'type': [1, 2, 3, 4,5 ], 
            'breed': [1,2,3,4,5],
            'status': [1, 2, 3], 
            'country': [1], 
            'age': [3, 1, 4, 2], 
            'size': [3, 2, 1, 4], 
            'gender': [2, 1], 
            'state': [1,2,3,4,5],
            'dateBegin': '2022-11-23', 
            'dateEnd': '2022-12-03', 
            'category': 'state'
        })
        sql = mock_sql.call_args.args[0]
        sql = ''.join(sql).lower()
        assert "type_id in (select id from temp_type)" in sql
        assert "breed_id in (select id from temp_breed)" in sql
        assert "age_id in (select id from temp_age)" in sql
        assert "gender_id in" in sql
        assert "country_id in (select id from temp_country)" in sql
        assert "status_id in (select id from temp_status)" in sql
        assert "state_id in (select id from temp_state)" in sql
        assert "size_id in (select id from temp_size)" in sql
        assert "group by state" in sql
        assert "date(published_at) between '2022-11-23 00:00:00' and '2022-12-03 00:00:00'" in sql
        assert json.loads(response.data) == {'ON': 12, 'SK':10, 'BC':5}

def test_get_heatmap(client):
    with patch('sql_util.execute_multiple_sql') as mock_sql:
        mock_sql.return_value = [(0, 'AB'), (1, 'BC'), (2, 'MB'), (3, 'NB'), (4, 'NL'), (5, 'NS'), (6, 'ON')]
        response = client.post('/V0/graph/heat', json= {
            'type': [8, 2, 6],
            'breed': [538, 539, 540], 
            'status': [1, 2], 
            'country': 'USA', 
            'age': [3, 1, 4], 
            'size': [3, 1], 
            'gender': [1, 2], 
            'dateBegin': '2022-11-23', 
            'dateEnd': '2022-12-03'
        })
        sql = mock_sql.call_args.args[0]
        sql = ''.join(sql).lower()
        assert "type_id in (select id from temp_type)" in sql
        assert "breed_id in (select id from temp_breed)" in sql
        assert "age_id in (select id from temp_age)" in sql
        assert "gender_id in" in sql
        assert "status_id in (select id from temp_status)" in sql
        assert "size_id in (select id from temp_size)" in sql
        assert "date(published_at) between '2022-11-23 00:00:00' and '2022-12-03 00:00:00'" in sql
        assert "country_id = 1" in sql
        assert json.loads(response.data) == {'AB':0, 'BC':1, 'MB':2, 'NB':3, 'NL':4, 'NS':5, 'ON':6}

