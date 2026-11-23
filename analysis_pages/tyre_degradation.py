import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

"""
 This file is responsible for creating and visualizing the selected drivers stint data
 on a certain tyre and the selected drivers' data will be visualized by different tabs.
 Underneath the charts there will be a table with the selected drivers' data.
"""

#############################
# Creating degradation chart
#############################
def create_degradation_chart(driver_plot_df, driver_stats_df, driver_name):
    """
     This function will construct a given driver's tire degradation chart.
     All the stints will be presented on one chart and all the different stints will have their own
     degradation line fitted on the stint's point cluster.
    """

    # Creating an empty plotly figure and a color scheme that will pick a different color for the stints
    fig    = go.Figure()
    colors = px.colors.qualitative.Plotly

    sorted_driver_stats = driver_stats_df.sort_values(by='Stint', ascending=True).reset_index(drop=True)

    # Iterating through the sorted regression rows
    for i, row in sorted_driver_stats.iterrows():
        # Getting hold of some data that will be used => we don't have to refer by dataframe and column
        stint     = row['Stint']
        compound  = row['Compound']
        slope     = row['Slope_steepness']
        intercept = row['Interception_point']

        # Putting the current stint's laps into a variable
        current_stint_laps = driver_plot_df[driver_plot_df['Stint'] == stint]

        # This will be in the legend's description
        stint_label = f"Stint {int(stint)} - {compound}"

        # Every point and its regression line will have the same color
        # The % division is for index error in case we would have more than 10 stints
        color = colors[i % len(colors)]

        # Adding the dot cluster to the initialized figure, with the customization
        fig.add_trace(go.Scatter(
            x          = current_stint_laps['LapNumber'],
            y          = current_stint_laps['LapTime_in_sec'],
            mode       = 'markers',
            name       = stint_label,
            legendgroup= stint_label,
            marker     = dict(color=color, size=5),
        ))

        # Reading the regression line's data into variables
        x_min = current_stint_laps['LapNumber'].min()
        x_max = current_stint_laps['LapNumber'].max()
        y_min = slope * current_stint_laps['TyreLife'].min() + intercept
        y_max = slope * current_stint_laps['TyreLife'].max() + intercept

        # Creating the regression line with the variables
        # showlegend=False -> bc it would cause to display the legends twice, one from the point cluster, one from the regression line
        fig.add_trace(go.Scatter(
            x           = [x_min, x_max],
            y           = [y_min, y_max],
            mode        = 'lines',
            name        = f"{stint_label} trend",
            legendgroup = stint_label,
            showlegend  = False,
            line        = dict(color=color, width=2),
        ))

    fig.update_layout(
        title        = f"{driver_name} - Tyre Degradation by stint",
        xaxis_title  = "Lap Number",
        yaxis_title  = "Lap Time (sec)",
        legend_title = "Legend"
    )

    return fig

###########################
# Plot rendering
###########################
def render_degradation_plot(plot_data, stats_data):
    """
     This function renders the degradation chart, and the selected drivers will have their own section.
    """
    st.header("Tyre Degradation")
    st.caption("Slowing means the line will have a positive steepness and negative in case if the fuel accelerates the car more than the tyre degradation slows it.")

    # In case the selected drivers have not enough data or have no data at all for a stint/stints
    # We warn the user that we don't have enough data for rendering a plot
    # Then we draw the division line and close it
    if (plot_data.empty) or (stats_data.empty):
        st.warning("Not enough data for rendering.")
        st.divider()
        return

    # Listing the drivers into a distinct list
    drivers_list = stats_data['Driver'].unique().tolist()
    # This one allows you to choose between the drivers
    tabs         = st.tabs(drivers_list)

    for tab, driver in zip(tabs, drivers_list):
        with tab:
            # Filtering two data frames for the current driver
            driver_plot  = plot_data[plot_data['Driver'] == driver]
            driver_stats = stats_data[stats_data['Driver'] == driver]

            # Generating a driver's plot with the func above
            figure = create_degradation_chart(driver_plot, driver_stats, driver)

            # Drawing the plot of the tab
            st.plotly_chart(figure, width='stretch')

    # Table representing the drivers' data under the chart
    st.subheader("Tyre degradation by stint summary table")
    # Rounding the numbers to three decimal place so every data will time data will have the same length
    st.dataframe(stats_data.round(3),
                 column_config={
                     'Stint_laps'         : "Tyre life",
                     'Slope_steepness'    : "Slow-down",
                     'Interception_point' : "Time",
                 },
                 width='stretch',
                 hide_index=True)

    st.divider()