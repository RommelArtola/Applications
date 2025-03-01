import streamlit as st
from pages_folder.linechart_page import show_linechart_page
from pages_folder.intro_page import show_intro

st.set_page_config(
    page_title="Healthcare Micro App",
    page_icon="🏥"
)

st.title('Micro Application: Healthcare Spend by Age, Sex, and Spend Details.')

intro_page, plotter_page = st.tabs(["📝 Intro", "📊 Line Chart"])

# Display content based on the selected tab
with intro_page:
    show_intro()

with plotter_page:
    show_linechart_page()