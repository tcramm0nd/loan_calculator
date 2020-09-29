import datetime as dt
import pandas as pd

class Loan:
    """Creates a Loan object using a loan amount, APR precentage, loan term,
    and, optionally, a start date (MM/DD/YYYY)"""
    def __init__(self, loan_amount, apr, term, start_date=None):

        self.initial_principal = loan_amount
        self.principal = loan_amount
        self.apr = apr / 100
        self.mpr = self.apr / 12
        self.initial_term = term * 12
        self.term_remaining = term * 12
        self.total_interest_paid = 0
        self.monthly_payment = round((loan_amount * self.mpr)/(1-(1+self.mpr) ** -self.initial_term), 2)
        if start_date:
            self.start_date = start_date
        else:
            self.start_date = dt.date.today()

    def update_payment(self):
        self.current_interest_payment = round((self.principal * self.mpr), 2)
        self.current_principal_payment = round((self.monthly_payment - self.current_interest_payment), 2)

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


    def amoritize(self):
        principal = self.principal
        term_remaining = self.term_remaining
        data = self._pay_off()
        self.amoritization_table = pd.DataFrame(data, columns=['Month No',
                                                    'Principal Remaining',
                                                    'Principal Payment',
                                                    'Interest Payment',
                                                    'Total Interest Paid'])
        self.amoritization_table.set_index('Month No', inplace=True)
        self.principal = principal
        self.term_remaining = term_remaining

        return self.amoritization_table


# class Amoritization(Loan):
#     """docstring for Amoritization."""
#
#     def __init__(self, Loan):
#         # super(Amoritization, self).__init__()
#         pass


def main():
    principal = input('Enter Loan Amount: ')
    principal = int(principal)
    apr = input('Enter APR Percentage: ')
    apr = float(apr)
    term = input('Enter Term in Years: ')
    term = int(term)

    loan = Loan(principal, apr, term)

    loan.amoritize()
    print(loan.amoritization_table)


if __name__ == "__main__":
    main()
