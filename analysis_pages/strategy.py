import plotly.express as px
import streamlit as st

compound_colors = {
    'SOFT'         : "#EE4B2B",
    'MEDIUM'       : "#FFEA00",
    'HARD'         : "#FFFFFF",
    'INTERMEDIATE' : "#66FF00",
    'WET'          : "#0096FF"
}

##################################
# Creating the base of the plot
##################################
def create_strategy_chart(plot_stint_df):
    """
     This function will create and return a horizontal plot of the selected drivers' tyre strategy.
     The calculations of the func will be based on the strategy_data.py's returned stint_length column.
    """
    # Creating a copy of the original dataframe
    plot_stint_df_copy = plot_stint_df.copy()

    # Getting the starting position of the bar
    plot_stint_df_copy['Bar_Start'] = plot_stint_df_copy['Start_Lap'] - 1

    # Creating the horizontal bar plots
    horizontal_bar_fig = px.bar(
        data_frame         = plot_stint_df_copy,
        x                  = 'Stint_Length',
        y                  = 'Driver',
        color              = 'Compound',
        color_discrete_map = compound_colors,
        base               = 'Bar_Start',
        orientation        = 'h',
        barmode            = 'overlay',
        hover_data         = ['Stint', 'Stint_Length', 'Start_Lap', 'Finish_Lap'],
        text               = 'Stint_Length',
        title              = "Tyre strategy by driver"
    )

    # Adding a black outline to all the bars -> if two consecutive laps are completed on the same compound they would seem to be one big stint
    horizontal_bar_fig.update_traces(marker_line_color='black', marker_line_width=1.5, textposition='inside')

    # Adding formatted title, not the column title itself
    horizontal_bar_fig.update_layout(
        xaxis_title  = "Lap Number",
        yaxis_title  = "Driver",
        legend_title = "Compound",
    )

    # Returning with the final plot
    return horizontal_bar_fig


####################################
# Generating the visual output
###################################
def render_strategy_plot(plot_stint_df, pit_loss_df, lost_pit_data):

    # Adding a header and a description to better understand what we see
    st.header("Strategy Bar Plot📊")
    st.caption("Bar plot with the different compounds used in the stints and how long they were on the cars.")

    # Filtering out the empty data
    if plot_stint_df.empty:
        st.warning("❌ No data to be rendered in the plot‼️")
        st.divider()
        return

    # Generating the bar chart
    strategy_chart = create_strategy_chart(plot_stint_df)
    st.plotly_chart(strategy_chart, width="stretch")

    st.subheader("Time Spent in Pit⏱️")
    st.caption("Table of the pit time - Pit In -> Pit Out - and the time difference to the fastest pit time out of the chosen drivers")

    # Checking if there are any missing data for the table and notifying the user in case if we have any
    if pit_loss_df.empty:
        st.info("❌ No data to render the table‼️")
    # Rendering the table from the data we get from the dataframe
    else:
        st.dataframe(pit_loss_df.round(3),
                     column_config={
                         'Pit_Time_sec'      : "Pit time (sec)",
                         'Pit_Lap'           : "Going to pit (Lap)",
                         'Delta_to_best_pit' : "Difference to fastest pit (ms)"
                     },
                     width="stretch",
                     hide_index=True)

    # If there are any missing pit data, we are notifying the user
    if lost_pit_data:
        with st.expander("❗Missing Pit Data, see more:"):
            for warning in lost_pit_data:
                st.warning(warning)

    # Signing the end of a section
    st.divider()
