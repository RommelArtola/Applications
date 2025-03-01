import streamlit as st


def show_intro():

    st.write("# Welcome to My Streamlit App! 👋")
    st.markdown(
        """
        The use of this application is to allow for end-user data exploration of a Health Care Spend dataset
        bucketed by Age Bucket, Sex, and Category spend.

        Additionally, the nominal spend data has been adjusted for inflation up to year 2020, so user can choose
        which spend value to visualize on their visuals.

        - Citations of Raw Data:
          * Centers for Medicare & Medicaid Services (2022). 
          Health Expenditures by State of Residence. Retrieved (2025-02-18) at 
          https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/age-and-sex
          
          * BLS CPI Inflation Dataset at
          https://data.bls.gov/timeseries/CUUR0000SA0

          
        ***Application developed by [Rommel Artola](https://www.linkedin.com/in/rommelartola/)***
    """
    )