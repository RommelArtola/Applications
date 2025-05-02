import pandas as pd



class Budget(object):
    def __init__(self, 
                 monthly_net_income, 
                 expected_annual_salary_increase_perc,
                 years

    ):
        self.annu_salary_bump_rt = expected_annual_salary_increase_perc / 100
        self.monthly_net = monthly_net_income
        self.years = years
        periods = self.years*12

        today = pd.Timestamp('today').replace(day=1).date()
        self.date_range = pd.date_range(start=today,
                                        periods=periods,
                                        freq='MS')
    def salary_bump(self, month_n):
        years_elapsed = month_n // 12
        salary = self.monthly_net * (1+self.annu_salary_bump_rt) ** years_elapsed
        return round(salary, 2)
    
    def schedule(self):
        data = []
        for i, date in enumerate(self.date_range):
            salary = self.salary_bump(i)
            row = {
                'Date': date,
                'Monthly Income': salary,
            }
            data.append(row)
        return pd.DataFrame(data)
