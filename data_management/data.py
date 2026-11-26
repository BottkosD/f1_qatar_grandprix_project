import os
import json
import pandas as pd

import fastf1
from pathlib import Path


"""
 This file is responsible for loading the f1 data, it loads it into cache if it does not exist yet,
 otherwise it loads the data from the cached file.
 It is also responsible for error handling when loading the data.
"""

######################
# Loading Configuration
######################
def load_config():
    print("Loading F1 connection configuration..")

    try:
        with open("data/connection_config.json", "r") as read_file:
            conf = json.load(read_file)

        os.environ['F1_USERNAME'] = conf['user_auth']['username']
        os.environ['F1_PASSWORD'] = conf['user_auth']['password']

        print("F1 configuration loaded Successfully!")

    except FileNotFoundError:
        print("The configuration file cannot be located, the F1 authentication cannot be done!")
    except KeyError:
        print("The file format is faulty the F1 authentication cannot be completed!")
    except Exception as e:
        print(f"An error occurred while loading the F1 data: {e}")


######################
# Loading F1 DB cached file
######################
def load_f1_data():
    load_config()
    print("Trying to load F1 data from cache..")

    try:
        f1_conf = Path("data/f1_race_details.json")

        if f1_conf.exists():
            with open(f1_conf, "r") as read_file:
                f1_details = json.load(read_file)

            year       = f1_details['race_details']['year']
            grandprix  = f1_details['race_details']['grandprix']
            identifier = f1_details['race_details']['identifier']

            cache_dir = Path('data/cache')
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
                print("Cache did not exist, cache created.")

            fastf1.Cache.enable_cache(str(cache_dir))

            try:
                print(f"Loading session: {year} - {grandprix} - race type: {identifier}")
                session = fastf1.get_session(year=year, gp=grandprix, identifier=identifier)
                session.load(telemetry=False, weather=False)

                laps            = session.laps # all the laps (from timing data) is queried
                data_to_be_used = f1_details['observed_data'] # needed col names loaded into a variable

                # Getting hold of the podium drivers' data
                podium = session.results.sort_values(by='Position').head(3).reset_index(drop=True)
                podium_df = pd.DataFrame({
                    'Position'   : podium['Position'].astype(int),
                    'Name'       : podium['LastName'],
                    'Image_path' : "pictures/drivers/" + podium['Abbreviation'] + ".png",
                })


                print("Session data loaded successfully!")
                return laps, data_to_be_used, podium_df

            except Exception as e:
                print(f"An error occurred while loading the F1 data: {e}")

    except FileNotFoundError as e:
        print(f"Error caught: {e}")
