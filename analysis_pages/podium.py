import streamlit as st


def render_podium(podium_df):
    if len(podium_df) < 3:
        st.warning("❌ Not enough data to render podium‼️")
        st.divider()
        return

    first = podium_df.iloc[0]
    second = podium_df.iloc[1]
    third = podium_df.iloc[2]

    left, col2, col1, col3, right = st.columns([1.5, 1, 1.2, 0.8, 1.5], vertical_alignment="bottom")

    # Rendering by position the drivers in a podium like style
    with col2:
        st.image(second['Image_path'], caption=f"🥈 {second['Position']} - {second['Name']}", width='stretch')

    with col1:
        st.image(first['Image_path'], caption=f"🥇 {first['Position']} - {first['Name']}", width='stretch')

    with col3:
        st.image(third['Image_path'], caption=f"🥉 {third['Position']} - {third['Name']}", width='stretch')

    st.divider()