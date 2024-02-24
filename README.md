# Warsaw Bus Position Analysis

The Warsaw Bus Position Analysis project aims to collect and analyze bus positions data from the Warsaw Public Transport API within specified time intervals. The analysis includes examining bus speeds and punctuality during peak and off-peak hours, as well as visualizing the data on a map of Warsaw.

# How to run
In demo.py file is a short example of how to use each module of project.

# Visualisation
1. Plot of average speed for each bus line in Warsaw.
![myplot](https://github.com/maktowon/bus_scraper/assets/108530595/396f89d2-76ab-4615-a76b-ae09cbaa4022)
2. Map with points where the average speed of the bus exceeds 50km/h.
![speed_over_50](https://github.com/maktowon/bus_scraper/assets/108530595/05e6295a-e304-4516-981a-28cc3e82731b)
3. Map with actual position of the bus and the expected position of the bus.
![location_diff](https://github.com/maktowon/bus_scraper/assets/108530595/73cbb7c2-cee8-4d6b-8c34-909d296388e4)

 
# File Structure
- Each directory in the src is python package.

- There are also tests included in the tests directory testing each module.
```
bus_scraper
├── demo
│   └── demo.py
├── README.md
├── src
│   ├── data_analysis
│   │   ├── DataAnalyser.py
│   │   └── __init__.py
│   ├── data_collection
│   │   ├── DataCollector.py
│   │   └── __init__.py
│   ├── data_parsing
│   │   ├── DataParser.py
│   │   └── __init__.py
│   ├── exceptions
│   │   ├── exceptions.py
│   │   └── __init__.py
│   └── models
│       ├── __init__.py
│       └── models.py
└── tests
    ├── analysis_tests
    │   └── test.py
    ├── collecting_tests
    │   └── test.py
    ├── model_tests
    │   └── test.py
    └── parsing_tests
        └── test.py
```
