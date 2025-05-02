import streamlit as st
import plotly.graph_objects as go
from main import Compare_Investments 
from functions import fmt_money


st.set_page_config(
    page_title="Investment Simulation App",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    "<h1 style='text-align: center;'>Buying Home vs Investing Simulation <br> 🏠vs📈</h1>",
    unsafe_allow_html=True
)


tabs = st.tabs(tabs=['Calculator', 'Info'])


with tabs[1]:
    st.markdown(
        """
        <div style='text-align: left; font-size: 16px; line-height: 1.6;'>

        <p>Welcome to my app! First, a brief introduction is in order.</p>

        <p>My name is Rommel Artola, and I'm a Data Scientist. I'm passionate about finding answers to 
            complicated questions and building things to make those decisions easier. 
            Feel free to connect with me on <a href='https://www.linkedin.com/in/rommelartola/' target='_blank'>Linkedin</a>!</p>
        
        <p>This app was inspired by a decision I'm currently weighing myself. With interest rates and home prices at all-time highs, 
        homeownership feels less like an "expected" milestone and more like a calculated investment decision (whatever that means)..</p>

        <p>This app lets you project and visualize the difference between owning a home and renting while investing in the stock market (via a low-cost index fund, for example)
            to help you decide which path might leave you with more value at the end.</p>

        <p>There are some limitations — most compounding values in this calculator happen consistently, while in real life they may not. Look at the historic trends of your specific values.
            For example, your rent might not increase one year, but this calculator assumes it always does. The same applies to a home's value and other investment.</p>

        <p>It's up to you to tweak the inputs and run different simulations based on your specific area and situation.</p>

        <p>To get the most out of this app, be sure to explore the “Optional Home Settings” section — this is where you can really tailor the experience to fit your situation.</p>

        <p>Each input has an info button (denoted by the “?” on the right). Hover over it if you ever have questions — there are detailed assumptions behind each input.</p>

        <p>If you have any questions, comments, concerns, or feedback, don't hesitate to reach out or connect using the Linkedin link above.</p>
        
        <p style='margin-top: 2em;'>Enjoy!</p>
        </div>
        """,
    unsafe_allow_html=True
    )


with tabs[0]:
    main_column1, main_column2 = st.columns(spec=2, gap='large', vertical_alignment='top', border=True)

    with main_column1: #Home options
        home_titles = st.markdown(body="### Home Options")

        home_price = st.number_input(label='Full Home Price', key='full_home_price',
                        min_value=0, max_value=None,
                        value=450_000, step=5_000,
                        help="This is the full price of the home you're considering.")

        home_down_payment = st.number_input(label="Home Down Payment", key='home_down_payment',
                        min_value=0, max_value=None,
                        value=int(450_000*.2), step=5_000, 
                        help="This is the down payment you're planning on using for the home loan.")

        home_loan_interest_perc = st.number_input(label="Loan Interest Rate", key='home_loan_interest_perc',
                        min_value=0.00, max_value=None,
                        value=4.5, step=0.05, 
                        help="Annual interest rate for the life of the loan. Assumes a fixed interest loan.")

        home_loan_years = st.segmented_control(label="Loan Years", key='home_loan_years',
                        options=[5, 15, 30], default=30,
                        help="Years the loan is borrowed for.")

        with st.expander(label='Optional Home Settings'):
            if home_down_payment/home_price >= .20:
                pmi_default = 0
            else:
                pmi_default = 300

            pmi_amount = st.number_input(label='Private Mortgage Insurance (PMI)', key='pmi_amount',
                            min_value=0, max_value=None,
                            value=pmi_default, step=50, 
                            help="This is the private mortgage insurance included in most traditional loans until at least 20% of the home total balance "
                            "has been paid. Code will automatically close out PMI when this target is reached.")

            other_monthly_home_fees = st.number_input(label='Other Monthly Home Fees', key='other_monthly_home_fees',
                            min_value=0, max_value=None,
                            value=0, step=500, 
                            help="Any other monthly home fees you'd like to add to the analysis. Things like property taxes "
                            "HOA, etc.. This value is not compounded in this analysis and is a fixed value for the life of the loan.")

            other_upfront_home_fees = st.number_input(label='Other One-Time Home Fees', key='other_upfront_home_fees',
                            min_value=0, max_value=None,
                            value=0, step=1_000, 
                            help="Any other ONE-TIME fees associated with the purchase of the home. Things like closing costs, any initial expected "
                            "repairs, etc...")
            
            home_value_compound = st.number_input(label="Expected Annual Home Appreciation Rate", key='home_appreciation_rate',
                            min_value=0.00, max_value=None,
                            value=0.00, step=0.05, 
                            help="Expected annual home appreciation rate. Compounded monthly. Critical field to compare equity vs investment "
                            "option.")


    with main_column2: # Investment Optios
        home_titles = st.markdown(body="### Investment Options")

        monthly_rent = st.number_input(label="Monthly Rent Value", key='monthly_rent',
                        min_value=0, max_value=None,
                        value=1_500, step=100, 
                        help="This is the monthly rental cost IF you decide to not purchase a home. This field is used "
                        "to calculate additional monthly contributions when the home monthly payments are higher than rental to keep things "
                        "as even as possible.")
        
        rent_compound = st.number_input(label="Expected Annual Rent Compounding Rate", key='rent_appreciation_rate',
                        min_value=0.00, max_value=None,
                        value=2.0, step=0.05, 
                        help="Expected annual rental compounding rate. This rental value is compounded every 12 months period, assuming "
                        "fixed 12-month rental agreements.")

        investment_compound = st.number_input(label="Expected Annual Investment Compounding Rate", key='investment_compounding_rate',
                        min_value=0.00, max_value=None,
                        value=8.5, step=0.05, 
                        help="Expected annual investment compounding rate (like the S&P500, for example). This value is compounding monthly")


    run_simulation = st.button("🚀 Run Comparison!", use_container_width=True, type='primary')
    st.divider()


    if run_simulation:
        #Load data
        compare = Compare_Investments(home_price=home_price,
                                    home_down_payment=home_down_payment,
                                    home_loan_interest_perc=home_loan_interest_perc,
                                    pmi_monthly_amt=pmi_amount,
                                    home_loan_years=home_loan_years,
                                    initial_additional_home_expenses=other_upfront_home_fees,
                                    annual_home_appreciation_perc=home_value_compound,
                                    other_fixed_monthly_payments=other_monthly_home_fees,
                                    annual_investment_growth_perc=investment_compound,
                                    monthly_rent_amt=monthly_rent,
                                    annual_rent_appreciation_perc=rent_compound)
        df = compare.create_comparison()


        # First show results KPI.
        final_row = df.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Final home equity", fmt_money(final_row["Home Expected Equity"]))
        col2.metric("Final investment balance", fmt_money(final_row["Investment Balance at End of Month"]))

        delta = final_row["Home Expected Equity"] - final_row["Investment Balance at End of Month"]
        verdict = "Home 🏠" if delta > 0 else "Investing 📈" if delta < 0 else "Tie 🤷🏽‍♂️"
        col3.metric("Best Option", value=verdict, delta=fmt_money(abs(delta)))




        # Show plot summary
        fig = go.Figure()

        # Add Home Equity line
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Home Expected Equity"],
            mode="lines",
            name="Home Equity Value",
            line=dict(width=5, color='#1f77b4')
        ))

        # Add Investment line
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Investment Balance at End of Month"],
            mode="lines",
            name="Investment Value",
            line=dict(width=5, dash='dot', color='#ff7f0e')  # dashed line for visual separation
        ))

        # Customize layout
        fig.update_layout(
            title="Equity in Home vs Investment Portfolio Over Time",
            xaxis_title="Date",
            yaxis_title="Value",
            yaxis_tickformat="$.2s",  # formats large numbers like 1.5M, 750K
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=20, l=40, r=20),
            height=500
        )

        # Show plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        #Show dataframe
        with st.expander("Show raw monthly schedule"):
            st.dataframe(df, use_container_width=True)


st.markdown(
    """
    <div style='text-align: right; font-size: 0.9em; margin-top: 50px;'>
        Created by <a href='https://www.linkedin.com/in/rommelartola/' target='_blank'>Rommel Artola</a>
    </div>
    """,
    unsafe_allow_html=True
)
