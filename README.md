# Warsaw Bus Position Analysis

The Warsaw Bus Position Analysis project aims to collect and analyze bus positions data from the Warsaw Public Transport API within specified time intervals. The analysis includes examining bus speeds and punctuality during peak and off-peak hours, as well as visualizing the data on a map of Warsaw.

# How to run
In demo.py file is a short example of how to use each module of project.

# Visualisation
1. Plot of average speed for each bus line in Warsaw.
![](/home/aktowon/Pictures/Screenshots/speed_over_50.png)
2. Map with points where the average speed of the bus exceeds 50km/h.
![](/home/aktowon/Pictures/Screenshots/location_diff.png)
3. Map with actual position of the bus and the expected position of the bus.
![](/home/aktowon/myplot.png)
 
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
