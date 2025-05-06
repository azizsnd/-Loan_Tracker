import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_annuity_schedule(principal, annual_rate, months):
    r = annual_rate / 100 / 12  # Monthly interest rate
    n = months

    # Calculate fixed monthly payment
    if r == 0:
        monthly_payment = principal / n
    else:
        monthly_payment = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    schedule = []
    remaining_principal = principal

    for m in range(1, months + 1):
        interest = remaining_principal * r
        principal_payment = monthly_payment - interest
        remaining_principal -= principal_payment

        schedule.append({
            "Month": m, 
            "Principal Payment (BGN)": round(principal_payment, 2),
            "Interest (BGN)": round(interest, 2),
            "Total Payment (BGN)": round(monthly_payment, 2),
            "Remaining Principal (BGN)": round(max(remaining_principal, 0), 2)
        })

    return pd.DataFrame(schedule)

# Global variables
loans = []
loans_table = None

def add_loan():
    """Add a new loan using the input values"""
    try:
        # Get values from input fields
        principal = float(loan_amount_entry.get())
        annual_rate = float(interest_rate_entry.get())
        months = int(loan_term_entry.get())
        description = description_entry.get()
        
        # Validate inputs
        if principal <= 0 or annual_rate < 0 or months <= 0:
            messagebox.showerror("Invalid Input", "Please enter positive values for amount, rate, and term")
            return
            
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter numeric values")
        return
    
    # Calculate schedule
    schedule = calculate_annuity_schedule(principal, annual_rate, months)
    
    # Get monthly payment from the first row of the schedule
    if not schedule.empty:
        monthly_payment = schedule.iloc[0]["Total Payment (BGN)"]
    else:
        monthly_payment = 0
    
    # Create loan object
    loan = {
        "principal": principal,
        "annual_rate": annual_rate,
        "months": months,
        "monthly_payment": monthly_payment,
        "description": description,
        "schedule": schedule
    }
    
    # Add to loans list
    loans.append(loan)
    
    # Add to treeview
    loans_table.insert("", "end", values=(
        f"{principal:.2f}",
        f"{annual_rate:.2f}",
        months,
        f"{monthly_payment:.2f}",
        description
    ))
    
    # Clear input fields
    loan_amount_entry.delete(0, tk.END)
    interest_rate_entry.delete(0, tk.END)
    loan_term_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    
    messagebox.showinfo("Success", "Loan added successfully")

def show_loan_details(event):
    """Display detailed information for the selected loan"""
    # Get selected item
    selected_item = loans_table.focus()
    if not selected_item:
        return
        
    # Get item index in the treeview
    index = loans_table.index(selected_item)
    
    # Get the loan
    loan = loans[index]
    
    # Create new window for details
    details_window = tk.Toplevel(root)
    details_window.title(f"Loan Details: {loan['description']}")
    details_window.geometry("900x500")
    
    # Loan summary information
    summary_frame = ttk.LabelFrame(details_window, text="Loan Summary")
    summary_frame.pack(fill=tk.X, padx=10, pady=10)
    
    summary_text = f"Principal: {loan['principal']:.2f} BGN | " \
                  f"Interest Rate: {loan['annual_rate']:.2f}% | " \
                  f"Term: {loan['months']} months | " \
                  f"Monthly Payment: {loan['monthly_payment']:.2f} BGN"
    
    ttk.Label(summary_frame, text=summary_text).pack(pady=5)
    
    # Frame for the schedule table
    table_frame = ttk.Frame(details_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create treeview for schedule
    columns = ("month", "principal", "interest", "payment", "remaining")
    schedule_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Define columns
    schedule_table.heading("month", text="Month")
    schedule_table.heading("principal", text="Principal Payment (BGN)")
    schedule_table.heading("interest", text="Interest (BGN)")
    schedule_table.heading("payment", text="Total Payment (BGN)")
    schedule_table.heading("remaining", text="Remaining Principal BGN")
    
    # Column widths
    for col in columns:
        schedule_table.column(col, width=150)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=schedule_table.yview)
    schedule_table.configure(yscrollcommand=scrollbar.set)
    
    # Pack table and scrollbar
    schedule_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Fill table with schedule data
    schedule = loan['schedule']
    for index, row in schedule.iterrows():
        schedule_table.insert("", "end", values=(
            int(row["Month"]),
            f"{row['Principal Payment (BGN)']:.2f}",
            f"{row['Interest (BGN)']:.2f}",
            f"{row['Total Payment (BGN)']:.2f}",
            f"{row['Remaining Principal BGN']:.2f}"
        ))
    
    # Calculate and display totals
    total_principal = schedule["Principal Payment (BGN)"].sum()
    total_interest = schedule["Interest (BGN)"].sum()
    total_payments = total_principal + total_interest
    
    totals_frame = ttk.LabelFrame(details_window, text="Payment Totals")
    totals_frame.pack(fill=tk.X, padx=10, pady=10)
    
    totals_text = f"Total Principal: {total_principal:.2f} BGN | " \
                 f"Total Interest: {total_interest:.2f} BGN | " \
                 f"Total Payments: {total_payments:.2f} BGN"
    
    ttk.Label(totals_frame, text=totals_text).pack(pady=5)

# Create the main window
root = tk.Tk()
root.title("Loan Tracker")
root.geometry("1000x500")

# Create a frame for the input area
input_frame = ttk.LabelFrame(root, text="Add New Loan", padding="10")
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

# Input fields
ttk.Label(input_frame, text="Loan Amount (BGN):").grid(row=0, column=0, sticky=tk.W, pady=5)
loan_amount_entry = ttk.Entry(input_frame, width=20)
loan_amount_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

ttk.Label(input_frame, text="Annual Interest Rate (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
interest_rate_entry = ttk.Entry(input_frame, width=20)
interest_rate_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

ttk.Label(input_frame, text="Loan Term (months):").grid(row=2, column=0, sticky=tk.W, pady=5)
loan_term_entry = ttk.Entry(input_frame, width=20)
loan_term_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

ttk.Label(input_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
description_entry = ttk.Entry(input_frame, width=20)
description_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

# Add loan button
ttk.Button(input_frame, text="Add Loan", command=add_loan).grid(row=4, column=0, columnspan=2, pady=10)

# Create a frame for the display area
display_frame = ttk.Frame(root)
display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Loans table title
ttk.Label(display_frame, text="Your Loans", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)

# Create treeview for loans
loans_table = ttk.Treeview(display_frame, columns=("amount", "rate", "term", "payment", "description"), 
                           show="headings", selectmode="browse")

# Define columns
loans_table.heading("amount", text="Loan Amount (BGN)")
loans_table.heading("rate", text="Interest Rate (%)")
loans_table.heading("term", text="Loan Term (months)")
loans_table.heading("payment", text="Monthly Payment (BGN)")
loans_table.heading("description", text="Description")

# Column widths
loans_table.column("amount", width=130)
loans_table.column("rate", width=100)
loans_table.column("term", width=130)
loans_table.column("payment", width=150)
loans_table.column("description", width=150)

# Scrollbar for loans table
scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=loans_table.yview)
loans_table.configure(yscrollcommand=scrollbar.set)

# Pack table and scrollbar
loans_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Bind double-click event to show loan details
loans_table.bind("<Double-1>", show_loan_details)

# Start the application
if __name__ == "__main__":
    root.mainloop()