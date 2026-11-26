"""
 This file is responsible for extracting the lap data of the specified drivers and the lap time of the
 whole field, which will draw out the difference between the drivers and the field.
 This will count the mean, median, standard deviation and minimum values for the picked drivers 
 and the whole field. 
 The calculate_pace function will also compute a delta col, as it is important for smooth comparison, 
 because the delta time eliminates the lap differences like the lightening factor coming from the less fuel.  
"""
def calculate_pace(cleaned_laps, picked_drivers, min_cars=5):
    #########################
    # Pace data calc
    #########################
    # This part will calculate the data for the plots to be used by the distinction of picked drivers and others from the field

    # Check if drivers are within the data
    driver_not_exists = set(picked_drivers) - set(cleaned_laps['Driver'])
    if driver_not_exists:
        raise ValueError("The drivers picked for the computations are not present in the specified json file.")

    # Creating copy of the existing data frame
    laps_df = cleaned_laps.copy()

    # Checks a row whether the driver is among the chosen one and returns a value
    def distinct_drivers(driver_name):
        if driver_name in picked_drivers:
            return driver_name
        else:
            return "Field"

    # In one step this creates a new column for the drivers that I picked to be labeled how they will be treated
    laps_df['Drivers_Group'] = laps_df['Driver'].apply(distinct_drivers)

    # Based on the lap number, we calculate median and the number of drivers, that will be a filtering criteria
    # .reset_index() is used bc we want the used cols to be put back into the data frame and not to throw away
    others    = laps_df[laps_df['Drivers_Group'] == "Field"]
    lap_stats = others.groupby('LapNumber')['LapTime_in_sec'].agg(['median', 'count']).reset_index()

    # Making sure that if we have less than 5 available driver stats in a lap, we throw it out, since it could cause some misleading information output
    lap_stats.loc[lap_stats['count'] < min_cars, 'median'] = None

    lap_stats = lap_stats.rename(columns={'median': 'Field_Lap_Median'})

    # Merging two further cols to the main data frame, double '[]' will leave out the 'count'
    laps_df = laps_df.merge(lap_stats[['LapNumber', 'Field_Lap_Median']], on='LapNumber', how='left')

    # Time delta calculation
    laps_df['Tdelta_to_Field'] = laps_df['LapTime_in_sec'] - laps_df['Field_Lap_Median']


    #########################################
    # Compound based comparison
    #########################################
    # This part will only show how good the drivers were based on the tire compound -> probably just going to be a table on representation

    # It is basically the same calculation as above we just calculate with the compound also
    stats_with_compound = laps_df.groupby(['Drivers_Group', 'Compound'])['LapTime_in_sec'].agg(['count', 'mean', 'median', 'min', 'std']).reset_index()

    # Renaming calculation cols for easier readability
    stats_with_compound = stats_with_compound.rename(columns={
        'count' : 'Count',
        'mean'  : 'Mean',
        'median': 'Median',
        'min'   : 'Minimum',
        'std'   : 'Standard Deviation',
    })

    # Calculating the whole Field's median based on the compound
    compound_median = others.groupby('Compound')['LapTime_in_sec'].median().reset_index()
    compound_median = compound_median.rename(columns={'LapTime_in_sec': 'Field_Compound_Median'})

    # Appending col to stats_with_compound
    stats_with_compound = stats_with_compound.merge(compound_median, on='Compound', how='left')

    # Gap calculation based on the compound grouped stats
    stats_with_compound['Gap_to_Field'] = stats_with_compound['Median'] - stats_with_compound['Field_Compound_Median']

    stats_with_compound = stats_with_compound.sort_values(by=['Compound', 'Gap_to_Field']).reset_index(drop=True)

    return laps_df, stats_with_compound


