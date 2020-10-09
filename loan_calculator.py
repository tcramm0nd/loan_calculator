import datetime as dt
import pandas as pd
from dateutil import parser
import csv

class Loan:
    """Creates a Loan object using a loan amount, APR precentage, loan term,
    and, optionally, a start date (MM/DD/YYYY)"""
    def __init__(self, loan_amount, apr, term, start_date=None, months=True):

        self.initial_principal = loan_amount
        self.principal = self.initial_principal
        self.apr_percent = apr
        self.apr = self.apr_percent / 100
        self.mpr = self.apr / 12
        self.months = months
        if months:
            self.initial_term = term
        else:
            self.initial_term = term * 12
        self.term_remaining = self.initial_term

        self.total_interest_paid = 0
        self.monthly_payment = round((loan_amount * self.mpr)/(1-(1+self.mpr) ** -self.initial_term), 2)
        if start_date:
            self.start_date = parser.parse(start_date)
        else:
            self.start_date = dt.date.today()

    def __str__(self):
        return f'''The monthly payment for a loan of {loan_amount} over {term}
              {term_unit}s at {apr} is {self.monthly_payment}'''

    def update_payment(self):
        self.current_interest_payment = self.principal * self.mpr
        self.current_principal_payment = self.monthly_payment - self.current_interest_payment

    def make_payment(self, regular=True, payment=0):
        if regular:
            self.update_payment()
            self.principal -= self.current_principal_payment
            self.term_remaining -= 1
            self.total_interest_paid += self.current_interest_payment
            self.principal = round(self.principal, 2)
            self.total_interest_paid = round(self.total_interest_paid, 2)
        else:
            self.principal -= payment

    def _pay_off(self):
        payments = []
        while self.principal > 0 and self.term_remaining > 0:
            self.make_payment()
            payments.append([(self.initial_term - self.term_remaining),
                             self.principal,
                             self.current_principal_payment,
                             self.current_interest_payment,
                             self.total_interest_paid])
        return payments

    def time_remaining(self, principal = 0.0):
        '''Returns the time remaining for a loan given a principal balance
        '''
        if principal != 0.0:
            self.principal = principal
        while self.principal > 0:
            self.make_payment()

        time_to_payoff = self.initial_term - self.term_remaining

        days_remaining = int(30.4 * time_to_payoff)
        payoff_date = dt.date.today() + dt.timedelta(days=days_remaining)
        print(payoff_date)
        return time_to_payoff




class Amoritization(Loan):
    """Creates an amoritization table for a Loan Object using pandas, that can
    also be saved to a csv"""

    def __init__(self, loan=None, loan_amount=0, apr=0, term=0):
        if loan:
            super().__init__(loan.initial_principal, loan.apr_percent,
                             loan.initial_term, start_date=loan.start_date, term_unit=loan.term_unit)
        else:
            super().__init__(loan_amount, apr, term)

        # principal = self.principal
        # term_remaining = self.term_remaining
        self.column_names =['Month No',
                            'Principal Remaining',
                            'Principal Payment',
                            'Interest Payment',
                            'Total Interest Paid']
        self.data = super()._pay_off()
        self.table = pd.DataFrame(self.data, columns=self.column_names)
        self.table.set_index('Month No', inplace=True)
        # self.principal = principal
        # self.term_remaining = term_remaining

        # return self.table

    def save(self, dir=None):
        headers = self.column_names
        rows = self.data
        file_name = f'Amoritization for a {self.initial_principal} loan.csv'
        with open(file_name, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)
