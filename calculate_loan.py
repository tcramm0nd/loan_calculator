from loan_calculator import Loan, Amoritization


def main():
    principal = input('Enter Loan Amount: ')
    principal = int(principal)
    apr = input('Enter APR Percentage: ')
    apr = float(apr)
    term = input('Enter Term in Months: ')
    term = int(term)

    loan = Loan(principal, apr, term)

    amoritization_table = Amoritization(loan)
    amoritization_table.save()


if __name__ == "__main__":
    main()
