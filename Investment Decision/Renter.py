import pandas as pd
import math

class Renting(object):
    def __init__(self, 
                 monthly_rent_cost, 
                 annual_rent_increase_perc,
                 years

    ):
        self.annu_rent_rt = annual_rent_increase_perc / 100
        self.monthly_rent = monthly_rent_cost
        self.years = years
        periods = self.years*12

        today = pd.Timestamp('today').replace(day=1).date()
        self.date_range = pd.date_range(start=today,
                                        periods=periods+1,
                                        freq='MS')
    def rent_value(self, month_n):
        years_elapsed = month_n // 12
        rent = self.monthly_rent * (1+self.annu_rent_rt) ** years_elapsed
        return math.ceil(rent)
    
    def schedule(self):
        data = []
        for i, date in enumerate(self.date_range):
            rent = self.rent_value(i)
            row = {
                'Date': date,
                'Rent Cost': rent,
            }
            data.append(row)
        return pd.DataFrame(data)