from src.data_parsing.DataParser import *
from src.data_collection.DataCollector import *
from src.data_analysis.DataAnalyser import *

if __name__ == '__main__':
    DC = DataCollector("your-api-key-goes-here")
    DP = DataParser()
    DA = DataAnalyser()

    DC.collect_all_data()

    DP.parse_bus_stops()
    DP.parse_actual_locations()
    DP.parse_expected_locations()

    DA.run_analysis()
