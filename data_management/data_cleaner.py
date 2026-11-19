import pandas as pd
from data_management.data import load_f1_data


"""
 The function is expecting to get raw data as 'laps' and the columns that has been chosen as the base of 
 the analysis.
 The function will drop all the laps with a value of NaN/NaT, the start lap, safety car and pit laps, so that
 there will not be any kind of peak data, just the pure race laptimes.
 The data to be used by the strategy part will be processed separately as it has a separate logic.
"""
def cleaned_laps_data(laps, cols=None):

    # Dropping data with not given value (NAT)
    cleaned_laps = laps.dropna(subset=['LapTime']).copy() # .copy() is needed, bc even if I assign the dataframe to a variable the dataframe referenced is still the same, not the copy

    # Dropping all the lap times considered inaccurate by the FIA
    # For example red flags, pits, (v)sc are considered inaccurate
    cleaned_laps = cleaned_laps[cleaned_laps["IsAccurate"] == True]
    # IsAccurate should remove all the generated data, just making sure that the generated data really is removed
    cleaned_laps = cleaned_laps[cleaned_laps["FastF1Generated"] == False]

    # converting lap times into seconds and adding it to the dataframe
    cleaned_laps['LapTime_in_sec'] = cleaned_laps['LapTime'].dt.total_seconds()

    # Checks if the cols argument is given and if so, it adds a new argument to be shown
    # As we have added the laptime_in_sec calculated column, we want to get hold of that data
    if cols is not None:
        chosen_fields = cols.copy()
        # Adding the laptime to the fields that will be retrieved
        chosen_fields.append('LapTime_in_sec')
        cleaned_laps = cleaned_laps[chosen_fields]

    return cleaned_laps
