import streamlit as st
import plotly.express as px

"""
 This file is responsible for rendering two outputs.
  - 1) The raw time data of the drivers on a linechart
  - 2) The time for the drivers on different compounds
"""

###########################
# Linechart creation
###########################
def create_pace_data_chart(laps_df):
    """
     This function returns with a linechart that will be used up in the next function that is responsible for the
     rendering of the linechart and a table with some other data.
    """

    # Filtering out the Field data, as we want to see the drivers
    laps_plot_df = laps_df[laps_df['Drivers_Group'] != 'Field'].copy()
    # Making sure the order of the laps are ok
    laps_plot_df = laps_plot_df.sort_values(by='LapNumber', ascending=True)

    # Defining data for the plot and customization of the plot
    fig = px.line(
        data_frame=laps_plot_df,
        x         ='LapNumber',
        y         ='Tdelta_to_Field',
        color     ='Drivers_Group',
        markers   =True,
        hover_data=['Compound', 'LapTime_in_sec'],
        title     ='Raw Pace Data',
        labels    ={
            'LapNumber'      : "Lap",
            'Tdelta_to_Field': "Time difference to Field (mp)",
            'Drivers_Group'  : "Driver"
        }
    )

    # Reversing the time delta will help better understand the plotted data -> the time showing the driver slowed down will be a descending line
    fig.update_yaxes(autorange='reversed', rangemode='tozero')

    # Dashed line to show the fields median
    fig.add_hline(y=0, line_dash='dash', line_color='gray', annotation_text="Field Median")

    return fig


###########################
# Table rendering
###########################
def render_pace_plot(laps_df, stats_with_compound):
    """
     This function is responsible for the rendering as mentioned above, that will use the create_pace_data_chart func and
     it will render also a table with different compounds used by the first three drivers and the time delta to the rest of the field.
    """
    st.header("Raw pace data")
    st.subheader("Performance of the first three drivers on the different compound they used and the difference in time with the Field.")

    # Saving the generated fig into a variable
    finished_fig = create_pace_data_chart(laps_df)

    # Rendering the linechart to be visible
    st.plotly_chart(finished_fig, width="stretch")

    # Table with driver stats
    st.subheader("First three drivers time difference on different compounds")


    rounded_compound_stats = round(stats_with_compound, 3).copy()
    st.dataframe(rounded_compound_stats, width="stretch", hide_index=True)

    # Visual division of the files -> creates a line from side to side of the page
    st.divider()
