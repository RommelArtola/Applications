import pandas as pd

class Amortizer(object):
    def __init__(self, 
                 home_price, 
                 down_payment_amt, 
                 pmi_monthly_amt,
                 other_fixed_monthly_home_payment,
                 loan_interest_perc, 
                 loan_terms_years,
                 annual_home_appreciation_perc,
    ):
        
        self.loan_amount = home_price - down_payment_amt
        self.down_payment = down_payment_amt
        self.home_value = home_price
        self.pmi_monthly_amt = pmi_monthly_amt
        self.other_monthly_pmts = other_fixed_monthly_home_payment
        
        self.loan_rt = loan_interest_perc / 100
        self.monthly_rt = self.loan_rt / 12
        self.appreciation_monthly_rate = annual_home_appreciation_perc / 100 / 12

        self.loan_terms_years = loan_terms_years
        self.loan_periods = self.loan_terms_years * 12


        start_date = pd.Timestamp('today').replace(day=1).date()
        self.date_range = pd.date_range(start=start_date,
                                        periods=self.loan_periods+1,
                                        freq='MS')

    def _calc_equal_monthly_payments(self,):
        """
        Uses class attributes, no parameters
        """
        numerator = self.monthly_rt * (1+self.monthly_rt) ** self.loan_periods
        denominator = ( (1+self.monthly_rt)**self.loan_periods) - 1
        
        #Equal Monthly Installments (EMI)
        if self.monthly_rt == 0.:
            EMI = self.loan_amount/self.loan_periods
        else:
            EMI = self.loan_amount * (numerator/denominator)

        return round(EMI, 2)
    
    def calc_interest_amt(self, outstanding_loan_amt, monthly_rate):
        return round(outstanding_loan_amt * monthly_rate, 2)
    
    def calc_principal_amt(self, EMI, interest_payment):
        ret = max(0, EMI-interest_payment)

        return round(ret, 2)

    def schedule(self):
        EMI = self._calc_equal_monthly_payments()
        
        data = []
        for i, date in enumerate(self.date_range):
            if i == 0:
                balance = self.loan_amount
                interest = 0.00
                principal = 0.00
                home_market_value = self.home_value
                
                row = {
                    'Date': date,
                    'Home Outstanding Balance': balance,
                    'Home Payment Amount': 0.00,
                    'Home Interest Payment': interest,
                    'Home Principal Payment': principal,
                    'Home PMI Payment': 0.00, #no payment first month
                    'Home Oth. Fixed Payments': 0.00, #no payment first month
                    'Home Total Monthly Payments': 0.00,
                    'Home Cumulative Interest Paid': 0.00,
                    'Home Cumulative Principal Paid': 0.00,
                    'Home Cumulative PMI Paid': 0.00,
                    'Home Cumulative Total Payments': 0.00,
                    'Home Expected Value': home_market_value,
                    'Home Expected Equity': home_market_value - balance
                }
            else:
                interest = self.calc_interest_amt(balance, monthly_rate=self.monthly_rt)
                principal = EMI - interest
                balance = max(0, balance - principal)
                home_market_value = round(home_market_value * (1+self.appreciation_monthly_rate), 2)
                
                if balance <= self.home_value * 0.80:
                    pmi = 0.00
                else:
                    pmi = self.pmi_monthly_amt
                
                total_payments_for_month = EMI + pmi + self.other_monthly_pmts

                cumu_interest_paid = sum(i['Home Interest Payment'] for i in data) + interest
                cumu_principal_paid = sum(i['Home Principal Payment'] for i in data) + principal
                cumu_pmi_paid = sum(i['Home PMI Payment'] for i in data) + pmi
                cumu_other_fixed_payments = sum(i['Home Oth. Fixed Payments'] for i in data) + self.other_monthly_pmts
                cumu_total_payments = cumu_interest_paid + cumu_principal_paid + cumu_pmi_paid + cumu_other_fixed_payments

                row = {
                    'Date': date,
                    'Home Outstanding Balance': balance,
                    'Home Payment Amount': EMI,
                    'Home Interest Payment': interest,
                    'Home Principal Payment': principal,
                    'Home PMI Payment': pmi,
                    'Home Oth. Fixed Payments': self.other_monthly_pmts,
                    'Home Total Monthly Payments': total_payments_for_month,
                    'Home Cumulative Interest Paid': cumu_interest_paid,
                    'Home Cumulative Principal Paid': cumu_principal_paid,
                    'Home Cumulative PMI Paid': cumu_pmi_paid,
                    'Home Cumulative Total Payments': cumu_total_payments,
                    'Home Expected Value': home_market_value,
                    'Home Expected Equity': home_market_value - balance,
                }
            data.append(row)

        return pd.DataFrame(data)
    

a = Amortizer(300_000,
              15_000,
              308,
              250,
              15,
              30,
              6)
a.schedule()