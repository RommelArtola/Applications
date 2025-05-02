import pandas as pd
import math

class Investment_Compounder(object):
    
    def __init__(self, 
                 initial_investment, 
                 years, 
                 annual_growth_rate_perc,
    ):
        """
        Assumes monthly compound rate
        """
                
        self.amt = initial_investment
        
        self.years = years
        self.periods = years * 12

        self.annu_rt = annual_growth_rate_perc / 100
        

        self.start_date = pd.Timestamp('today').replace(day=1).date()
        self.date_range = pd.date_range(start=self.start_date,
                                        periods=self.periods+1,
                                        freq='MS')

    def schedule(self, monthly_rents, total_monthly_payments):
        """
        Returns a list of monthly compounding iteration
        Assumes contributions are at beginning of month and take into account the compounding
        for the time period.
        """        

        ret = []
        for i, (rent, home) in enumerate(zip(monthly_rents, total_monthly_payments)):
            if i == 0:
                extra_investable_by_not_buying = max(0, home-rent)
                initial_balance = self.amt + extra_investable_by_not_buying
                total_before_interest = initial_balance
                interest = round(total_before_interest * (self.annu_rt / 12), 2)
                compounded = initial_balance + interest
                #First Row
                new_row = {
                    'Date': self.date_range[i],
                    'Investment Initial Balance': initial_balance,
                    'Investment Additional by Not Buying': extra_investable_by_not_buying, 
                    'Investment Interest Earned': interest,
                    'Investment Balance at End of Month': compounded,
                }

            else:
                extra_investable_by_not_buying = max(0, home-rent)
                initial_balance = compounded
                total_before_interest = initial_balance + extra_investable_by_not_buying
                interest = round(total_before_interest * (self.annu_rt / 12), 2)
                compounded = total_before_interest + interest
            
                new_row = {
                    'Date': self.date_range[i],
                    'Investment Initial Balance': initial_balance,
                    'Investment Additional by Not Buying': extra_investable_by_not_buying, 
                    'Investment Interest Earned': interest,
                    'Investment Balance at End of Month': compounded,
                }

            ret.append(new_row)
        
        return pd.DataFrame(ret)


# a = Investment_Compounder(25_000,
#                           30,
#                           8)

# a.schedule([6000]*361,
#            [2200]*361,
#            [2800]*361
#            )

