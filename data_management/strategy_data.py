import pandas as pd


"""
 This file will make its own data cleaning, bc here we will need also the pit in and pit out time to calculate the
 time spent in the box.
 The file will also return the tyre types used with the laps the drivers spent on them.
"""


def get_strategy_data(raw_laps, picked_drivers):
    # The function uses the raw data for the visualization bc we need the time the driver spent in the box

    # Copying the raw_laps filtered by the picked drivers
    filtered_raw_laps = raw_laps[raw_laps['Driver'].isin(picked_drivers)].copy()

    # Lists for the two returning data
    stint_history = []
    pit_loss      = []
    lost_pit_data = []

    grouped_data_by_driver = filtered_raw_laps.groupby('Driver')

    ################################
    # Calc of pit time
    ################################

    for driver, driver_data in grouped_data_by_driver:
        previous_pit_in = None

        # Drivers data grouped by the stint
        ddata_grouped_by_stint = driver_data.groupby('Stint')

        for stint_num, stint_data in ddata_grouped_by_stint:
            # Checking idf the driver went into the box in the previous lap
            if previous_pit_in is not None:
                # -> if this one is evaluated true then it means this line will contain a 'pit-out' time
                pit_out_timestamp = stint_data['PitOutTime'].iloc[0]

                # If the pit-out time exists we compute the difference of the two timestamps that results in the time spent in the box
                if pd.notna(pit_out_timestamp):
                    pit_time = (pit_out_timestamp - previous_pit_in).total_seconds()

                    pit_calculated_data = {
                        'Driver'    : driver,
                        'Stint'     : stint_num,
                        'PitOutTime': pit_time,
                    }

                    pit_loss.append(pit_calculated_data)
                else:
                    # In case of a missing pit in time we provide a message saying some data is lost
                    message = f"Missing Pit out time for {driver} at stint {stint_num}!"
                    lost_pit_data.append(message)

                previous_pit_in = None


            ##############################
            # Getting the tyre compounds
            ##############################
            # Tyre data for the graph
            tyre_compound       = stint_data['Compound'].iloc[0]
            compound_start_lap  = stint_data['LapNumber'].min()
            compound_finish_lap = stint_data['LapNumber'].max()

            # Getting the extracted data into a dict for better handling
            compound_by_driver = {
                'Driver'     : driver,
                'Stint'      : stint_num,
                'Compound'   : tyre_compound,
                'Start_Lap'  : compound_start_lap,
                'Finish_Lap' : compound_finish_lap,
            }

            stint_history.append(compound_by_driver)

            # Searching for the pit-in time at the last record of the current stint
            current_pit_in = stint_data['PitInTime'].iloc[-1]
            if pd.notna(previous_pit_in):
                previous_pit_in = current_pit_in


    plot_stint_df = pd.DataFrame(stint_history)
    pit_loss_df   = pd.DataFrame(pit_loss)

    return plot_stint_df, pit_loss_df, lost_pit_data
