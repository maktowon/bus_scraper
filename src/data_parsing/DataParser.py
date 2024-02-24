import os
import pandas as pd
import json


def process_stop_record(record):
    latitude = ""
    longitude = ""
    post = ""
    group_id = ""

    stop_data_list = record["values"]
    for stop_data in stop_data_list:
        if stop_data["key"] == "szer_geo":
            latitude = float(stop_data["value"])
        elif stop_data["key"] == "dlug_geo":
            longitude = float(stop_data["value"])
        elif stop_data["key"] == "slupek":
            post = stop_data["value"]
        elif stop_data["key"] == "zespol":
            group_id = stop_data["value"]

    return group_id, post, latitude, longitude


class DataParser:
    def __init__(self):
        self.actual_positions_directory = "data/actual_bus_location"
        self.expected_positions_directory = "data/expected_bus_location"
        self.parsed_data_directory = "parsed_data"
        self.unparsed_bus_stops = "data/bus_stops.json"

    def parse_actual_locations(self):
        dfs = []

        for file_name in os.listdir(self.actual_positions_directory):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.actual_positions_directory, file_name)
                df = pd.read_json(file_path)
                dfs.append(df)

        all_actual_df = pd.concat(dfs, ignore_index=True)
        all_actual_df = all_actual_df[['Lines', 'Brigade', 'Time', 'Lon', 'Lat']]
        all_actual_df.rename(columns={'Lines': 'Line', 'Lon': 'Longitude', 'Lat': 'Latitude'}, inplace=True)

        file = os.listdir(self.actual_positions_directory)[0]
        one_point_df = pd.read_json(os.path.join(self.actual_positions_directory, file))
        one_point_df = one_point_df[['Lines', 'Brigade', 'Time', 'Lon', 'Lat']]
        one_point_df.rename(columns={'Lines': 'Line', 'Lon': 'Longitude', 'Lat': 'Latitude'}, inplace=True)

        output_directory = os.path.join(self.parsed_data_directory, "actual_bus_location")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_filepath = os.path.join(output_directory, "actual_bus_location.csv")
        all_actual_df.to_csv(output_filepath, index=False)

        output_filepath = os.path.join(output_directory, "one_time_location.csv")
        one_point_df.to_csv(output_filepath, index=False)

    def parse_bus_stops(self):
        bus_stops_data = []
        with open(self.unparsed_bus_stops) as file:
            json_data = json.load(file)

            for record in json_data:
                id, post, latitude, longitude = process_stop_record(record)
                bus_stop_info = {
                    "id": id,
                    "post": post,
                    "latitude": latitude,
                    "longitude": longitude
                }
                bus_stops_data.append(bus_stop_info)

            bus_stops_df = pd.DataFrame(bus_stops_data)

            if not os.path.exists(self.parsed_data_directory):
                os.makedirs(self.parsed_data_directory)

            output_filepath = os.path.join(self.parsed_data_directory, "bus_stops.csv")
            bus_stops_df.to_csv(output_filepath, index=False)

    def parse_expected_locations(self):
        bus_stops_filepath = os.path.join(self.parsed_data_directory, "bus_stops.csv")
        bus_stops_df = pd.read_csv(bus_stops_filepath)

        for directory_name in os.listdir(self.expected_positions_directory):
            directory_path = os.path.join(self.expected_positions_directory, directory_name)
            line = directory_name

            if os.path.isdir(directory_path):
                data_list = []

                for file_name in os.listdir(directory_path):
                    if file_name.endswith(".json"):
                        file_path = os.path.join(directory_path, file_name)

                        id_post = file_name.split("_")
                        id_value = id_post[0]
                        post_value = int(id_post[1].split(".")[0])

                        stop_info = bus_stops_df[
                            (bus_stops_df["id"] == id_value) & (bus_stops_df["post"] == post_value)]
                        with open(file_path, 'r') as file:
                            json_data = json.load(file)

                            for record in json_data:
                                data = record["values"]
                                brigade = ""
                                time = ""
                                for item in data:
                                    if item["key"] == "brygada":
                                        brigade = item["value"]
                                    elif item["key"] == "czas":
                                        time = item["value"]

                                if not stop_info.empty:
                                    longitude = stop_info.iloc[0]["longitude"]
                                    latitude = stop_info.iloc[0]["latitude"]
                                    data_list.append([line, brigade, time, longitude, latitude])

                df = pd.DataFrame(data_list, columns=["Line", "Brigade", "Time", "Longitude", "Latitude"])

                output_directory = os.path.join(self.parsed_data_directory, "expected_bus_location", line)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                output_filepath = os.path.join(output_directory, "expected_location.csv")
                df.to_csv(output_filepath, index=False)
