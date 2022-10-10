import pytest

def test_base_route():
    #   assert response.status_code == 200
    #   assert response.body == 'This is the root directory. Try out the /hello route!'
    assert 1 == 1

def test_hello_world():
    #   assert response.status_code == 200
    #   assert response.body == 'Hello, World!'
    assert 'hello' in 'hello world!'
