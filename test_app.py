import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from unittest.mock import patch
import pandas as pd

# Assuming your Flask app is named `app` and is in `app.py`
from app import app, get_env_variable

@pytest.fixture
def client():
    # Set up the Flask test client
    with app.test_client() as client:
        yield client

@patch('app.pd.read_sql_table')
def test_get_data_success(mock_read_sql_table, client: FlaskClient):
    # Mock the return value of pd.read_sql_table
    mock_data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })
    mock_read_sql_table.return_value = mock_data

    # Make a GET request to the /data endpoint
    response = client.get('/data')
    response_data = response.get_json()

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the returned data matches the mock data
    expected_data = [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 30},
        {'id': 3, 'name': 'Charlie', 'age': 35}
    ]
    assert response_data == expected_data

@patch('app.pd.read_sql_table')
def test_get_data_failure(mock_read_sql_table, client: FlaskClient):
    # Mock the pd.read_sql_table to raise an exception
    mock_read_sql_table.side_effect = Exception("Database error")

    # Make a GET request to the /data endpoint
    response = client.get('/data')
    response_data = response.get_json()

    # Assert that the response status code is 500 (Internal Server Error)
    assert response.status_code == 500

    # Assert that the error message is returned
    assert response_data['error'] == "Database error"
