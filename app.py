import json
import streamlit as st

############################
# Importing modules
############################
from data_management.data import load_f1_data
from data_management.data_cleaner import cleaned_laps_data
from data_management.pace_data import calculate_pace
from data_management.tdegradation_data import calculate_degradation
from data_management.strategy_data import get_strategy_data
from analysis_pages.pace import render_pace_plot
from analysis_pages.tyre_degradation import render_degradation_plot
from analysis_pages.strategy import render_strategy_plot
from analysis_pages.podium import render_podium


#########################
# Page Setup
#########################
st.set_page_config(page_title="Formula 1 - Qatar Grand Prix", layout="wide")
st.title("🏎️ F1 Qatar Grand Prix Analysis 📊")

# Reading the first three pilots from the .json file
with open("data\\f1_race_details.json", "r", encoding="utf-8") as f:
    config = json.load(f)

podium_drivers = config["picked_drivers"]

#Loading and cleaning the data and caching it, so it doesn't have to be loaded again every time
@st.cache_data(show_spinner="Loading F1 race data...")
def load_and_clean_data():
    raw_laps, observed_cols, podium_df = load_f1_data()
    cleaned_data = cleaned_laps_data(raw_laps, observed_cols)
    return raw_laps, cleaned_data, podium_df

raw_laps, cleaned_laps, podium_df = load_and_clean_data()

# Rendering the podium section at the top of the page
render_podium(podium_df)

# Sidebar choice filter for user input
st.sidebar.header("Driver Filter:")
all_drivers = sorted(cleaned_laps["Driver"].unique().tolist())

# Making suer the default selected drivers from the .json file are in the database
default_drivers = [d for d in podium_drivers if d in all_drivers]

# Limiting the number of drivers to be able to calculate the Field columns
selected_drivers = st.sidebar.multiselect(
    label          = "Maximum drivers selected: 5",
    options        = all_drivers,
    default        = default_drivers,
    max_selections = 5,
)

# Rendering the analysis pages
if selected_drivers:
    #Rendering the pace section
    laps_df, stats_with_compound = calculate_pace(cleaned_laps, selected_drivers)
    render_pace_plot(laps_df, stats_with_compound)

    #Rendering the tyre degradation section
    plot_data, stats_data = calculate_degradation(cleaned_laps, selected_drivers)
    render_degradation_plot(plot_data, stats_data)

    # Rendering the strategy section
    plot_stint_df, pit_loss_df, lost_pit_data = get_strategy_data(raw_laps, selected_drivers)
    render_strategy_plot(plot_stint_df, pit_loss_df, lost_pit_data)
else:
    st.warning("📢 Please choose at least one driver in the sidebar filter!")


