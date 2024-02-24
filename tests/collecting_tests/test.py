import os
import json
import shutil
from unittest.mock import patch, mock_open

from _pytest import unittest

from src.data_collection.DataCollector import DataCollector


@patch('src.data_collection.DataCollector._request_data')
def test_fetch_stops(mock_request_data):
    apikey = 'test_api_key'
    collector = DataCollector(apikey)

    mock_request_data.return_value = {'stops': 'data'}

    collector._fetch_stops()

    assert os.path.exists('data')

    expected_params = {
        "id": collector.stops_resource_id,
        "apikey": apikey,
    }
    mock_request_data.assert_called_with(collector.stops_endpoint, expected_params)

    filepath = os.path.join('data', 'bus_stops.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
        assert data == mock_request_data.return_value

    shutil.rmtree("data")


@patch('src.data_collection.DataCollector._request_data')
def test_fetch_routes(mock_request_data):
    apikey = 'test_api_key'
    collector = DataCollector(apikey)

    mock_request_data.return_value = {'routes': 'data'}

    collector._fetch_routes()

    assert os.path.exists('data')

    expected_params = {
        "apikey": apikey,
    }
    mock_request_data.assert_called_with(collector.routes_endpoint, expected_params)

    filepath = os.path.join('data', 'routes.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
        assert data == mock_request_data.return_value

    shutil.rmtree("data")


@patch('src.data_collection.DataCollector._request_data')
def test_fetch_locations(mock_request_data):
    apikey = 'test_api_key'
    collector = DataCollector(apikey)
    sample_size = 1

    mock_request_data.return_value = {'some': 'data'}

    collector._fetch_locations(sample_size)

    assert os.path.exists('data/actual_bus_location')

    assert mock_request_data.call_count == sample_size

    expected_params = {
        "resource_id": collector.location_resource_id,
        "type": 1,
        "apikey": apikey,
    }
    mock_request_data.assert_called_with(collector.location_endpoint, expected_params)

    shutil.rmtree("data")


if __name__ == '__main__':
    unittest.main()
