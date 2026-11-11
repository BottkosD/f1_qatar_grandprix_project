import pandas as pd
import numpy as np


########################
# Outlier data removal
########################

def remove_outlier_data(stint_df):
    """
     The function gets the stint of a driver, calculates the upper and lower quartile based on the LapTime_in_sec col.
     The func will determine the upper border - as we do not need the lower border, bc a driver will not be magically faster -
     with IQR => IQR = (Q3-Q1) -> Upper border = Q3 + (1.5 * IQR).
     The data frame will only contain the data lower or equal to the determined value.
    """

    # Calculating the Q1 and Q3
    lower_bound = stint_df['LapTime_in_sec'].quantile(0.25)
    upper_bound = stint_df['LapTime_in_sec'].quantile(0.75)

    # IQR calculation
    iqr_value = upper_bound - lower_bound

    # Determining the upper border with the IQR
    upper_border = upper_bound + (1.5 * iqr_value)

    # Filtering the stint_df
    stint_df = stint_df[stint_df['LapTime_in_sec'] <= upper_border].copy()

    return stint_df


########################
# Tyre degradation calc
########################

def calculate_degradation(cleaned_laps, picked_drivers):
    """
     The function groups the data by drivers, compounds and stints.
     It filters based on the remove_outlier_data func, too short stints, outliers will be removed, also calculates
     the degradation of the tires.
     The output is composed of 2 dataframes, one for the points of the scatterplot and one for the regression line.
    """

    # As calculating the stints for the Field would have no sense, only the picked drivers data is considered
    cleaned_laps_pdrivers = cleaned_laps[cleaned_laps['Driver'].isin(picked_drivers)].copy()

    cleaned_stints_list    = []
    degradation_stats_list = []

    # Grouping the data based on driver, compound, stints
    grouped_drivers = cleaned_laps_pdrivers.groupby(['Driver', 'Compound', 'Stint'])

    # Iterating through the grouped drivers by the labels and the data of the labels
    for (driv, comp, stin), data in grouped_drivers:
        # Removing the outlier data, not a problem if we do not filter, bc grouping does not return with an empty dataframe
        outlier_check_result = remove_outlier_data(data)

        # The minimum advised number of data for regression computation is 4-5
        if len(outlier_check_result) >= 5:
            # Appending the cleaned data to our data
            cleaned_stints_list.append(outlier_check_result)

            # Axis point variables -> we save the data that will be represented on the scatterplot and getting the data on which base we will count the slope
            x_axis = outlier_check_result['TyreLife']
            y_axis = outlier_check_result['LapTime_in_sec']

            # Getting the important results for the slope's steepness and the interception point (where y=0)
            slope, intercept = np.polyfit(x_axis, y_axis, 1)

            data_per_stint = {
                'Driver'            : driv,
                'Compound'          : comp,
                'Stint'             : stin,
                'Stint_laps'        : len(outlier_check_result),
                'Slope_steepness'   : slope,
                'Interception_point': intercept,
            }

            degradation_stats_list.append(data_per_stint)

    # After the iteration we put the dataframes into one
    if cleaned_stints_list:
        plot_data = pd.concat(cleaned_stints_list, ignore_index=True)
    else:
        plot_data = pd.DataFrame()

    # Making a dataframe from the list of dictionaries
    if degradation_stats_list:
        stats_data = pd.DataFrame(degradation_stats_list)
    else:
        stats_data = pd.DataFrame()

    return plot_data, stats_data

