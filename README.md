# Loan Tracker Application

A Python application that helps manage and track personal loans. This application calculates monthly payments using the annuity formula and provides detailed repayment schedules.

## Features

- Add new loans with principal amount, interest rate, term, and description
- Calculate monthly payments automatically
- View all loans in a table
- See detailed repayment schedules for each loan
- Track principal and interest over the loan term

## Requirements

- Python 3.6 or higher
- Required packages: pandas, tkinter

## How to Use

1. Clone this repository
2. Install required packages: `pip install pandas`
3. Run the application: `python loan_tracker.py`
4. Enter loan details and click "Add Loan"
5. Double-click on any loan to view its detailed repayment schedule

## Implementation Details

This application implements the annuity formula:
A = P × [r(1+r)^n / ((1+r)^n - 1)]

Where:
- A = Monthly payment
- P = Loan principal
- r = Monthly interest rate (annual rate ÷ 12 ÷ 100)
- n = Total number of months

