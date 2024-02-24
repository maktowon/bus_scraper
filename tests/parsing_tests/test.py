import shutil
import unittest
import os
import json
from src.data_parsing.DataParser import DataParser


class TestDataParser(unittest.TestCase):
    def setUp(self):
        # Set up the directory paths
        self.actual_positions_directory = "data/actual_bus_location"
        self.expected_positions_directory = "data/expected_bus_location"
        self.parsed_data_directory = "parsed_data"
        self.unparsed_bus_stops = "data/bus_stops.json"

        os.makedirs(self.actual_positions_directory, exist_ok=True)
        os.makedirs(self.parsed_data_directory, exist_ok=True)

        actual_data = [
            {"Lines": "Line1", "Brigade": "B1", "Time": "10:00", "Lon": 1.0, "Lat": 2.0},
            {"Lines": "Line2", "Brigade": "B2", "Time": "11:00", "Lon": 3.0, "Lat": 4.0}
        ]
        for i in range(2):
            with open(os.path.join(self.actual_positions_directory, f"actual_location_{i}.json"), 'w') as f:
                json.dump(actual_data, f)

        expected_data = [
            {
                "values": [
                    {
                        "value": "null",
                        "key": "symbol_2"
                    },
                    {
                        "value": "null",
                        "key": "symbol_1"
                    },
                    {
                        "value": "015",
                        "key": "brygada"
                    },
                    {
                        "value": "Banacha",
                        "key": "kierunek"
                    },
                    {
                        "value": "TD-2BAN",
                        "key": "trasa"
                    },
                    {
                        "value": "03:56:00",
                        "key": "czas"
                    }
                ]
            }
        ]
        for i in range(2):
            os.makedirs(os.path.join(self.expected_positions_directory, f"{i + 1}"), exist_ok=True)
            with open(os.path.join(self.expected_positions_directory, f"{i + 1}", f"{i + 1}_{i + 1}.json"), 'w') as f:
                json.dump(expected_data, f)

        bus_stops_data = [
            {
                "values": [
                    {
                        "value": "1001",
                        "key": "zespol"
                    },
                    {
                        "value": "01",
                        "key": "slupek"
                    },
                    {
                        "value": "Kijowska",
                        "key": "nazwa_zespolu"
                    },
                    {
                        "value": "2201",
                        "key": "id_ulicy"
                    },
                    {
                        "value": "52.248455",
                        "key": "szer_geo"
                    },
                    {
                        "value": "21.044827",
                        "key": "dlug_geo"
                    },
                    {
                        "value": "al.Zieleniecka",
                        "key": "kierunek"
                    },
                    {
                        "value": "2023-10-21 00:00:00.0",
                        "key": "obowiazuje_od"
                    }
                ]
            }
        ]

        with open(self.unparsed_bus_stops, 'w') as f:
            json.dump(bus_stops_data, f)

    # Write your test cases here

    def tearDown(self):
        shutil.rmtree("data")
        shutil.rmtree("parsed_data")

    def test_parse_actual_locations(self):
        parser = DataParser()

        parser.parse_actual_locations()

        self.assertTrue(os.path.exists(
            os.path.join(parser.parsed_data_directory, "actual_bus_location", "actual_bus_location.csv")))
        self.assertTrue(
            os.path.exists(os.path.join(parser.parsed_data_directory, "actual_bus_location", "one_time_location.csv")))

    def test_parse_bus_stops(self):
        parser = DataParser()

        parser.parse_bus_stops()

        self.assertTrue(os.path.exists(os.path.join(parser.parsed_data_directory, "bus_stops.csv")))

    def test_parse_expected_locations(self):
        parser = DataParser()

        parser.parse_bus_stops()
        parser.parse_expected_locations()

        self.assertTrue(os.path.exists(
            os.path.join(parser.parsed_data_directory, "expected_bus_location", "1", "expected_location.csv")))
        self.assertTrue(os.path.exists(
            os.path.join(parser.parsed_data_directory, "expected_bus_location", "2", "expected_location.csv")))


if __name__ == "__main__":
    unittest.main()
