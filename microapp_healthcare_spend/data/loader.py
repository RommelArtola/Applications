import pandas as pd
import numpy as np
import streamlit as st
import os


# Get average CPI per year so we can adjust for inflation

file_repo = os.path.dirname(__file__)
BLS_CPI_FILEPATH = os.path.join(file_repo, 'BLS CPI Dataset.xlsx')
AGE_AND_SEX_FILEPATH = os.path.join(file_repo, 'Age and Sex dataset.csv')

# @st.cache_data
def load_data():
    cpi_df = (
        pd.read_excel(BLS_CPI_FILEPATH, skiprows=11)
        .assign(
            AVG_CPI = lambda df: np.mean(df[df.columns[1:]], axis=1)
        )
        .filter(items=['Year', 'AVG_CPI'])
    )


    health_spend_df = (
        pd.read_csv(AGE_AND_SEX_FILEPATH)
        #Filter out all the total values
        .pipe(lambda df: df[ (df['Payer'] != 'Total')
                            & (df['Age Group'] != 'Total')
                            & (df['Sex'] != 'Total')
                            & (df['Service'] != 'Total Personal Health Care')
                            ] )
        .melt(id_vars=['Payer', 'Service', 'Age Group', 'Sex'],
            value_vars=[str(i) for i in range(2002, 2022, 2)], 
            value_name='Nominal Spend', 
            var_name='Year')
        .astype({'Year': int})
        .merge(cpi_df, how='left', on='Year')
        .assign(
            CPI_2020 = cpi_df[cpi_df['Year'] == 2020]['AVG_CPI'].values[0],
            Inflation_Adj_Spend = lambda df: df['Nominal Spend'] / (df['AVG_CPI'] / df['CPI_2020']),
        ) 

        .filter(items=['Year', 'Payer', 'Service', 'Age Group', 'Sex', 'Nominal Spend', 'Inflation_Adj_Spend'])
    )

    return health_spend_df