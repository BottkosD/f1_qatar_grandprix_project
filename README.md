# 🏎️ F1 Qatar Grand Prix Analysis Dashboard

## What You can see in the interactive streamlit dashboard:
- At the top of the page You can see the first three drivers in a podium like allocation, with a picture of them and the place they achieved.
- Scrolling down You can see a plot of the drivers' time performance, with a table that contains some specific data about how they performed respect to the other chosen drivers and the Field.
- Below that You will find a Scatter plot with a cluster of points of a stint and all the clusters, that represent a stint have their own regression line. Depending on the regression line's steepness, if it is positive, the tyre degradation had a higher effect on the time, while if You see a negative steepness it means, that the emptying fuel tank outweighed the slow-down effect of the tyre degradation.
- Under the Scatter plot You can find a table the scatter plot worked with, and is formatted for better readability.
- The last plot is showing how the teams played with the different tyre compounds showing for the viewer on a Bar plot how many laps each driver has done on a compound and when they changed to a compound.
- At the bottom of the page You will see the last table that occupies with the pit times, the gap of each driver to the fastest pit time out of the chosen drivers, when they left the pit.

## Specification about functionality:
- By default, the top three drivers are picked and their data is represented on the plots and tables.
- On the sidebar You can choose from the drivers of the race, BUT only 5 drivers can be picked at a time, for assuring that the Field has enough drivers to work with.
- In case of not choosing a single driver, the webpage will warn the user to choose at least one driver, while the page does not render out any plots.
- In case of missing values at specific parts of the dashboard the code informs the user that because of missing value(s) a specific part, a line or data is not shown.
- Important for the usage You have to create the data/connection_config.json based on the connection_config.example.json file.

## Installation and Usage:
### Setup:
1.) Clone the repository
```bash
git clone https://github.com/<your-username>/f1_qatar_grandprix_project.git
cd f1_qatar_grandprix_project
```

2.) Create and then activate the virtual env
```bash
python -m venv .venv
# depending on what you have use one of these commands:
# Win: .venv\Scripts\activate.bat
# Unix: source .venv/bin/activate
```

3.) Install the required packages
```bash
pip install -r requirements.txt
```

4.) Run the program
```bash
streamlit run app.py
```
The dashboard will open in your browser by default at http://localhost:8501

## Structure:
```text
f1_qatar_grandprix_project/
├── analysis_pages/           # UI configuration and rendering
│   ├── pace.py
│   ├── podium.py
│   ├── strategy.py
│   └── tyre_degradation.py
├── data/                     # Here is stored the fastf1 cache, connection data and the specified arguments of the database
│   └── f1_race_details.json
│   └── connection_config.example.json # Example of how the connection_config.json file has to be created here
├── data_management/          # Data management for the plotting files   
│   ├── data.py               # Loading in data
│   ├── data_cleaner.py       # Cleaning the loaded data 
│   ├── pace_data.py
│   ├── strategy_data.py
│   └── tdegradation_data.py
├── pictures/                 # Pictures of the drivers
│   └── drivers/              
├── app.py                    # File that calls to life the whole code
├── requirements.txt          
├── .gitignore
└── README.md 
```
