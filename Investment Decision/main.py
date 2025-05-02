import pandas as pd
from Amortizer import Amortizer
from Investment import Investment_Compounder
from Renter import Renting
# import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

class Compare_Investments(object):
    """
    Compares two investment classes. Classes are structured
    with language and variables that it is meant to compare
    the purchase of a home VS a traditional investment like the SP500 
    index fund. 
    """
    def __init__(self, 
                 home_price,
                 home_down_payment,
                 home_loan_interest_perc,
                 pmi_monthly_amt,
                 home_loan_years,
                 initial_additional_home_expenses,
                 annual_home_appreciation_perc,
                 other_fixed_monthly_payments,
                 annual_investment_growth_perc, 
                 monthly_rent_amt,
                 annual_rent_appreciation_perc,        
    ):
        

        self.home_investment = Amortizer(home_price=home_price,
                                         down_payment_amt=home_down_payment,
                                         pmi_monthly_amt=pmi_monthly_amt,
                                         other_fixed_monthly_home_payment=other_fixed_monthly_payments,
                                         loan_interest_perc=home_loan_interest_perc,
                                         loan_terms_years=home_loan_years,
                                         annual_home_appreciation_perc=annual_home_appreciation_perc)
        
        self.rent_table = Renting(monthly_rent_cost=monthly_rent_amt,
                                  annual_rent_increase_perc=annual_rent_appreciation_perc,
                                  years=home_loan_years)


        initial_investment = home_down_payment + initial_additional_home_expenses
        self.alternative_investment = Investment_Compounder(initial_investment=initial_investment,
                                                  years=home_loan_years,
                                                  annual_growth_rate_perc=annual_investment_growth_perc)
        

        

        self.income_df = pd.DataFrame({})
        self.home_schedule_df = pd.DataFrame({})
        self.investment_df = pd.DataFrame({})
        self.renting_df = pd.DataFrame({})
    
    def create_amortization_schedule(self):
        self.home_schedule_df = self.home_investment.schedule()
        return self.home_schedule_df
    
    
    def create_rent_schedule(self):
        self.renting_df = self.rent_table.schedule()
        return self.renting_df

    def create_investment_schedule(self):
        total_month_home_expenses = self.home_schedule_df['Home Total Monthly Payments']
        monthly_rents = self.renting_df['Rent Cost']

        self.investment_df = self.alternative_investment.schedule(monthly_rents=monthly_rents,
                                                                  total_monthly_payments=total_month_home_expenses)
        return self.investment_df

    def create_comparison(self, plot:bool):
        rent = self.create_rent_schedule()
        home = self.create_amortization_schedule()
        investment = self.create_investment_schedule()

        df = (
            rent
            .merge(right=home, how='inner', on='Date')
            .merge(right=investment, how='inner', on='Date')
            .assign(
                Date = lambda df: pd.to_datetime(df['Date']).dt.date,
            )
        )
        

        if plot == True:
            plot_df = df[['Date', 'Home Expected Equity', 'Investment Balance at End of Month']]

            fig, ax = plt.subplots(figsize=(10, 6))

            sns.lineplot(data=plot_df, x='Date', y='Home Expected Equity', label='Home Equity Value', ax=ax)
            sns.lineplot(data=plot_df, x='Date', y='Investment Balance at End of Month', label='Investment Value', ax=ax)

            # format y-axis for millions
            ax.yaxis.set_major_formatter(
                mtick.FuncFormatter(lambda x, pos: f'{x/1_000_000:.1f} M')
            )
            plt.show()


        return df
    

# home_price = 320_000
# home_down_payment = 20_000
# monthly_pmi = 450
# other_home_fees = 500
# home_loan_interest_perc = 7.5
# home_loan_years = 30
# annual_home_appreciation_perc = 4.5
# initial_additional_home_expenses = home_price * 0.01 #closing costs, etc.

# annual_investment_growth_perc = 8.5
# monthly_rent = 1950
# annual_rent_increase_perc = 2.25




# a = Compare_Investments(home_price=home_price,
#                         home_down_payment=home_down_payment,
#                         pmi_monthly_amt=monthly_pmi,
#                         other_fixed_monthly_payments=other_home_fees,
#                         home_loan_interest_perc=home_loan_interest_perc,
#                         home_loan_years=home_loan_years,
#                         annual_home_appreciation_perc=annual_home_appreciation_perc,
#                         annual_investment_growth_perc=annual_investment_growth_perc,
#                         monthly_rent_amt=monthly_rent,
#                         annual_rent_appreciation_perc=annual_rent_increase_perc,
#                         initial_additional_home_expenses=initial_additional_home_expenses
#                         )
# df = a.create_comparison(plot=True)
# df