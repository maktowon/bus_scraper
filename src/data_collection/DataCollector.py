from typing import Union, Dict, Any, Set, List, Tuple
import time
import json
import requests
import os

from src.models.models import *


class DataCollector:
    def __init__(self, apikey: str) -> None:
        self.apikey = apikey
        self.location_endpoint = "https://api.um.warszawa.pl/api/action/busestrams_get"
        self.schedule_endpoint = "https://api.um.warszawa.pl/api/action/dbtimetable_get"
        self.routes_endpoint = "https://api.um.warszawa.pl/api/action/public_transport_routes"
        self.stops_endpoint = "https://api.um.warszawa.pl/api/action/dbstore_get"
        self.location_resource_id = "f2e5503e-927d-4ad3-9500-4ab9e55deb59"
        self.schedule_resource_id = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"
        self.stops_resource_id = "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3"
        self.stops: List[Stop] = []
        self.stop_map: Dict[Tuple[str, str, str], Stop] = {}
        self.line_to_stop_map: Dict[str, Set[Stop]] = {}

    def _fetch_locations(self, sample_size: int = 10) -> None:
        directory = "data/actual_bus_location"
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(1, sample_size + 1):
            file_name = os.path.join(directory, f"{i}.json")
            params: Dict[str, Union[str, int, None]] = {
                "resource_id": self.location_resource_id,
                "type": 1,
                "apikey": self.apikey,
            }

            while True:
                r = _request_data(self.location_endpoint, params)
                if r != "B\u0142\u0119dna metoda lub parametry wywo\u0142ania":
                    with open(file_name, 'w') as f:
                        json.dump(r, f, indent=4)
                    break
                else:
                    time.sleep(1)

            time.sleep(10)

    def _fetch_stops(self) -> None:
        directory = "data"
        filename = "bus_stops.json"
        if not os.path.exists(directory):
            os.makedirs(directory)

        params: Dict[str, Union[str, int, None]] = {
            "id": self.stops_resource_id,
            "apikey": self.apikey,
        }
        r = _request_data(self.stops_endpoint, params)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            json.dump(r, f, indent=4)

    def _fetch_routes(self) -> None:
        directory = "data"
        filename = "routes.json"
        if not os.path.exists(directory):
            os.makedirs(directory)

        params: Dict[str, Union[str, int, None]] = {
            "apikey": self.apikey,
        }
        r = _request_data(self.routes_endpoint, params)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as file:
            json.dump(r, file, indent=4)

    def collect_all_data(self, intervals: int = 10) -> None:
        self._fetch_locations(intervals)
        self._fetch_stops()
        self._fetch_routes()
        self._get_stops_for_line()
        self._fetch_expected_locations()

    def _get_stops(self) -> None:
        file_path = "data/bus_stops.json"

        if not os.path.exists(file_path):
            raise FileNotExistsException(file_path)

        with open(file_path, 'r') as file:
            json_data = json.load(file)

        for record in json_data:
            new_stop = process_stop_record(record)
            self.stops.append(new_stop)

        self.create_stop_mapping()

    def _fetch_expected_locations_for_line_at_stop(self, line: str, stop: Stop, refetch: bool = False) -> None:
        stop_id = stop.group_id
        post = stop.post
        directory = os.path.join("data/expected_bus_location", line)
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not refetch:
            return

        file_name = os.path.join(directory, f"{stop_id}_{post}.json")

        if not os.path.exists(file_name):
            params = {
                "id": self.schedule_resource_id,
                "busstopId": stop_id,
                "busstopNr": post,
                "line": line,
                "apikey": self.apikey
            }
            success = False
            while not success:
                try:
                    r = _request_data(self.schedule_endpoint, params)
                    with open(file_name, 'w') as file:
                        json.dump(r, file, indent=4)
                    success = True
                except FetchingDataApiException as e:
                    print(f"Error fetching data for {file_name}: {e.status_code}")
                    time.sleep(1)
                    continue

    def _fetch_expected_locations_for_line(self, line: str, stops: Set[Stop], refetch: bool = False) -> None:
        for stop in stops:
            self._fetch_expected_locations_for_line_at_stop(line, stop, refetch)

    def _fetch_expected_locations(self, refetch: bool = False) -> None:
        self._get_stops_for_line()
        directory = "data/expected_bus_location"
        if not os.path.exists(directory):
            os.makedirs(directory)

        for line, stops in self.line_to_stop_map.items():
            self._fetch_expected_locations_for_line(line, stops, refetch)

    def _get_stops_for_line(self) -> None:
        self._get_stops()
        filepath = "data/routes.json"
        with open(filepath, "r") as file:
            json_data = json.load(file)

        for line, line_data in json_data.items():
            # discard SKM trains and trams
            if line.startswith("S") or len(line) < 3:
                continue
            stops_for_line: Set[Stop] = set()
            for _, route_data in line_data.items():
                for _, stop_data in route_data.items():
                    street_id = stop_data["ulica_id"]
                    group_id = stop_data["nr_zespolu"]
                    stop_number = stop_data["nr_przystanku"]
                    key = street_id, group_id, stop_number
                    stop = self.stop_map.get(key)
                    if stop:
                        stops_for_line.add(stop)

            self.line_to_stop_map[line] = stops_for_line

    def create_stop_mapping(self) -> None:
        for stop in self.stops:
            key = (stop.street_id, stop.group_id, stop.post)
            self.stop_map[key] = stop


def _request_data(url: str, params: Dict[str, Union[str, int, None]]) -> Any:
    r = requests.get(url=url, params=params)
    if r.status_code == requests.codes.ok:
        response = r.json()
    else:
        print(f"Error fetching data from {url}, status: {r.status_code}")
        raise FetchingDataApiException(r.url, r.status_code)

    if response.get("error"):
        print(response["error"])
        raise Exception(response["error"])

    return response["result"]


def custom_sort_key(key):
    if isinstance(key, str):
        return len(key), key
    else:
        return key


def sort_json(json_data):
    if isinstance(json_data, dict):
        sorted_dict = {}
        for key in sorted(json_data.keys(), key=custom_sort_key):
            sorted_dict[key] = sort_json(json_data[key])
        return sorted_dict
    elif isinstance(json_data, list):
        return [sort_json(item) for item in json_data]
    else:
        return json_data


def process_stop_record(record):
    latitude = ""
    longitude = ""
    name = ""
    post = ""
    street_id = ""
    group_id = ""

    stop_data_list = record["values"]
    for stop_data in stop_data_list:
        if stop_data["key"] == "szer_geo":
            latitude = float(stop_data["value"])
        elif stop_data["key"] == "dlug_geo":
            longitude = float(stop_data["value"])
        elif stop_data["key"] == "nazwa_zespolu":
            name = stop_data["value"]
        elif stop_data["key"] == "slupek":
            post = stop_data["value"]
        elif stop_data["key"] == "id_ulicy":
            street_id = stop_data["value"]
        elif stop_data["key"] == "zespol":
            group_id = stop_data["value"]

    location = Location(longitude=longitude, latitude=latitude)
    new_stop = Stop(name=name, location=location, post=post, street_id=street_id, group_id=group_id)
    return new_stop
