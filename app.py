def calculate_nz_tax(income):
    if income <= 14000:
        tax = income * 0.105
    elif income <= 48000:
        tax = 14000 * 0.105 + (income - 14000) * 0.175
    elif income <= 70000:
        tax = (
            14000 * 0.105 +
            (48000 - 14000) * 0.175 +
            (income - 48000) * 0.30
        )
    elif income <= 180000:
        tax = (
            14000 * 0.105 +
            (48000 - 14000) * 0.175 +
            (70000 - 48000) * 0.30 +
            (income - 70000) * 0.33
        )
    else:
        tax = (
            14000 * 0.105 +
            (48000 - 14000) * 0.175 +
            (70000 - 48000) * 0.30 +
            (180000 - 70000) * 0.33 +
            (income - 180000) * 0.39
        )
    return tax

def calculate_acc_levy(income):
    acc_rate = 0.0153
    acc_income_cap = 142283
    return min(income, acc_income_cap) * acc_rate

def calculate_kiwisaver(income, percent):
    return income * (percent / 100)

def calculate_student_loan(income):
    threshold = 22828
    return max(0, (income - threshold) * 0.12)

# Get user input
try:
    income = float(input("Enter your annual income (NZD): $"))
    kiwisaver_percent = float(input("Enter your KiwiSaver contribution (%) [e.g., 3, 6]: "))
    student_loan_input = input("Do you have a student loan? (yes/no): ").strip().lower()
    has_student_loan = student_loan_input in ['yes', 'y']
except ValueError:
    print("Invalid input. Please enter numeric values.")
    exit()

# Calculate deductions
income_tax = calculate_nz_tax(income)
acc_levy = calculate_acc_levy(income)
kiwisaver = calculate_kiwisaver(income, kiwisaver_percent)
student_loan = calculate_student_loan(income) if has_student_loan else 0

total_deductions = income_tax + acc_levy + kiwisaver + student_loan
annual_take_home = income - total_deductions
fortnightly_take_home = annual_take_home / 26
monthly_take_home = annual_take_home / 12
monthly_deductions = total_deductions / 12

# Output
print("\n📌 Summary of Annual and Periodic Deductions:")
print(f"Income Tax:             ${income_tax:,.2f}")
print(f"ACC Levy:               ${acc_levy:,.2f}")
print(f"KiwiSaver ({kiwisaver_percent}%):     ${kiwisaver:,.2f}")
if has_student_loan:
    print(f"Student Loan Repayment: ${student_loan:,.2f}")
print("--------------------------------------------------")
print(f"Total Annual Deductions: ${total_deductions:,.2f}")
print(f"Monthly Deductions:      ${monthly_deductions:,.2f}")
print(f"Fortnightly Take-Home Pay: ${fortnightly_take_home:,.2f}")
print(f"Monthly Take-Home Pay:     ${monthly_take_home:,.2f}")
