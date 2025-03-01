import streamlit as st
from data.loader import load_data

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker




def show_linechart_page():
    df = load_data()

    #Initilization
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = df

    NOM_OR_ADJ = st.radio(label='Nominal or Adjusted Spend?', options=['Nominal', 'Adjusted'])

    
    HUE_VAR = st.selectbox(label='Hue (Legend) Variable', 
                           options=[None, 'Payer', 'Age Group', 'Service', 'Sex'],
                           index=0)

    spend_col = 'Nominal Spend' if NOM_OR_ADJ == 'Nominal' else 'Inflation_Adj_Spend'
    agg_col = 'Total_Nominal_Spend' if NOM_OR_ADJ == 'Nominal' else 'Total_Adjusted_Spend'
    title_plot = 'Total Spend Over Time' + (' (Nominal Spend)' if NOM_OR_ADJ == 'Nominal' else ' (Adjusted for Inflation)')

    group_by_cols = ['Year']

    if HUE_VAR:
        group_by_cols.append(HUE_VAR)

    display_df = (
        st.session_state['dataframe']
        .groupby(by=group_by_cols, as_index=False)
        .agg(**{agg_col: (spend_col, 'sum')})
        .astype({'Year': int,
                agg_col: float})
    )
    display_df[agg_col] = display_df[agg_col] / 1_000
    
    cols = display_df.columns.tolist()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.pointplot(data=display_df, x='Year', y=agg_col, hue=HUE_VAR, ax=ax, errorbar=None)
    
    ax.xaxis.get_major_locator().set_params(integer=True)

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Spend (in $ Billions)')
    ax.set_title(title_plot)
    ax.grid(True, axis='y')
    st.pyplot(fig=fig)


    st.markdown(
        """
        Key Takeaways:
        * To no surprise, healthcare continues to be an ever-increasing cost.
        * The Payer "Other Payers and Programs" had a sharp increase from 2018-2020 which looks to be out of the norm
        * After a rapid increase from 2014-2016, Private Health Insurance spend (inflation-adjusted) seems to be flat-lining/showing potential sings of future relative decrease.
        * Age group 65-84 has seen a faster rate of growth than other groups lately, and may soon become the highest-spending age group if trends continue

        Limitations:
        * Total spend not calculated per capita, so increases in cost could be, at least in part, due to an increase 
            in population size rather than just a net spend increase.

        """
    )
