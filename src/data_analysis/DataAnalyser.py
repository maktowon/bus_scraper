from datetime import datetime, timedelta

from src.exceptions.exceptions import FileNotExistsException
import os
import glob
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import folium


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)

    R = 6371.0

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


class DataAnalyser:
    def __init__(self):
        self.actual_positions_filepath = "parsed_data/actual_bus_location/actual_bus_location.csv"
        self.actual_one_time_position = "parsed_data/actual_bus_location/actual_bus_location.csv"
        self.expected_positions_directory = "parsed_data/expected_bus_location"

    def analyze_actual_position_file(self):
        if not os.path.exists("analysed_data"):
            os.makedirs("analysed_data")

        df = pd.read_csv(self.actual_positions_filepath)

        grouped = df.groupby(['Line', 'Brigade'])
        line_speeds = []
        high_speed_locations = []

        for group_name, group_data in grouped:
            group_data = group_data.sort_values(by='Time')

            first_row = group_data.iloc[0]
            last_row = group_data.iloc[-1]

            distance = calculate_distance(first_row['Latitude'], first_row['Longitude'],
                                          last_row['Latitude'], last_row['Longitude'])

            time_diff = (pd.to_datetime(last_row['Time']) - pd.to_datetime(first_row['Time'])).total_seconds()

            if time_diff > 0:
                average_speed = distance / (time_diff / 3600)
                if 0 < average_speed < 100:
                    line_speeds.append({'Line': group_name[0], 'Average Speed': average_speed})
                if 100 > average_speed > 50:
                    high_speed_locations.append((last_row['Latitude'], last_row['Longitude']))

        line_speeds_df = pd.DataFrame(line_speeds)
        self.line_speeds_df = line_speeds_df

        line_avg_speeds = line_speeds_df.groupby('Line')['Average Speed'].mean()

        overall_avg_speed = line_speeds_df['Average Speed'].mean()

        plt.figure(figsize=(50, 6))
        line_avg_speeds.plot(kind='bar', xlabel='Line', ylabel='Average Speed (km/h)',
                             title='Average Speed for Each Line')
        plt.axhline(y=overall_avg_speed, color='r', linestyle='--', label='Overall Average Speed')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig("analysed_data/plot.png")

        map_center = high_speed_locations[0] if high_speed_locations else (0, 0)
        m = folium.Map(location=map_center, zoom_start=10)

        for location in high_speed_locations:
            folium.Marker(location).add_to(m)

        map_file_path = "analysed_data/speed_map.html"
        m.save(map_file_path)

    def traverse_expected_positions(self):
        if not os.path.exists(self.expected_positions_directory):
            raise FileNotExistsException(self.expected_positions_directory)

        print("Expected Positions Directory:")
        csv_files = glob.glob(os.path.join(self.expected_positions_directory, '*.csv'))
        for file_path in csv_files:
            print(os.path.basename(file_path))

    def load_actual_positions(self):
        self.actual_df = pd.read_csv(self.actual_one_time_position)
        self.actual_df['Time'] = pd.to_datetime(self.actual_df['Time'])

    def find_nearest_expected_location(self, line, brigade, time):
        if line.startswith('N'):
            return None, None
        expected_positions_filepath = os.path.join(self.expected_positions_directory, str(line),
                                                   "expected_location.csv")
        if os.path.exists(expected_positions_filepath):
            expected_df = pd.read_csv(expected_positions_filepath)
            mask = ~(expected_df['Time'].astype(str).str.startswith(('24', '25')))
            expected_df = expected_df[mask]
            current_date = datetime.today().date() - timedelta(days=1)
            expected_df['Time'] = pd.to_datetime(current_date.strftime('%Y-%m-%d') + ' ' + expected_df['Time'])
            filtered_df = expected_df[(expected_df['Brigade'] == int(brigade))]
            if not filtered_df.empty:
                nearest_row = filtered_df.iloc[(filtered_df['Time'] - time).abs().argsort()[0]]
                return nearest_row['Latitude'], nearest_row['Longitude']
        return None, None

    def mark_on_map(self):
        m = folium.Map(location=[52.2297, 21.0122], zoom_start=12)

        for _, row in self.actual_df.iterrows():
            try:
                lat, lon = row['Latitude'], row['Longitude']
                line, brigade = row['Line'], row['Brigade']
                time = row['Time']
                expected_lat, expected_lon = self.find_nearest_expected_location(line, brigade, time)
                lat1, lon1 = row['Latitude'], row['Longitude']
                lat2, lon2 = expected_lat, expected_lon
                points = [(lat1, lon1), (lat2, lon2)]
                if expected_lat is not None and expected_lon is not None:
                    folium.Marker([expected_lat, expected_lon], popup=f"Actual Position {line}, {brigade}",
                                  icon=folium.Icon(color='green')).add_to(m)
                    folium.Marker([lat, lon], popup=f"Actual Position {line}, {brigade}",
                                  icon=folium.Icon(color='blue')).add_to(m)
                    folium.PolyLine(points, color='red', weight=2.5, opacity=1).add_to(m)
            except Exception as e:
                continue

        m.save('parsed_data/positon_map.html')

    def run_analysis(self):
        self.analyze_actual_position_file()
        self.load_actual_positions()
        self.mark_on_map()
