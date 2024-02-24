import shutil
import unittest
import pandas as pd
import os
from src.data_analysis.DataAnalyser import DataAnalyser


class TestDataAnalyser(unittest.TestCase):
    def setUp(self):
        self.data_analyser = DataAnalyser()

        test_data = {
            'Line': [213, 213, 187, 187, 1, 1, 2, 2],
            'Brigade': [3, 3, 5, 5, 1, 1, 2, 2],
            'Time': ['2024-02-23 21:33:45', '2024-02-23 21:33:45', '2024-02-23 21:34:06', '2024-02-23 21:36:26',
                     '2024-02-23 21:34:06', '2024-02-23 21:36:26', '2024-02-23 21:34:06', '2024-02-23 21:36:26'],
            'Longitude': [21.213174, 21.213174, 21.0691376, 21.0693727, 100.0, 200.0, 0.0, 0.0],
            'Latitude': [52.161233, 52.161233, 52.1813956, 52.1812512, 100.0, 200.0, 0.0, 0.0]
        }

        self.test_df = pd.DataFrame(test_data)

        os.makedirs("parsed_data/actual_bus_location", exist_ok=True)

        self.test_df.to_csv(self.data_analyser.actual_positions_filepath, index=False)

    def test_analyze_actual_position_file_1(self):
        self.data_analyser.analyze_actual_position_file()

        self.assertTrue(os.path.exists("analysed_data/plot.png"))

    def test_analyze_actual_position_file_2(self):
        self.data_analyser.analyze_actual_position_file()

        self.assertTrue(os.path.exists("analysed_data/plot.png"))

        self.assertEqual(len(self.data_analyser.line_speeds_df), 1)  # Two lines in test data

    def tearDown(self):
        shutil.rmtree("analysed_data")
        shutil.rmtree("parsed_data")


if __name__ == '__main__':
    unittest.main()
