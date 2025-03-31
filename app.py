import streamlit as st

# ────────────────────────────────────────────────
# Helper functions for calculations
# ────────────────────────────────────────────────

def calculate_nz_tax(income):
    if income <= 14000:
        return income * 0.105
    elif income <= 48000:
        return 14000 * 0.105 + (income - 14000) * 0.175
    elif income <= 70000:
        return 14000 * 0.105 + (48000 - 14000) * 0.175 + (income - 48000) * 0.30
    elif income <= 180000:
        return 14000 * 0.105 + (48000 - 14000) * 0.175 + (70000 - 48000) * 0.30 + (income - 70000) * 0.33
    else:
        return 14000 * 0.105 + (48000 - 14000) * 0.175 + (70000 - 48000) * 0.30 + (180000 - 70000) * 0.33 + (income - 180000) * 0.39

def calculate_acc_levy(income):
    return min(income, 142283) * 0.0153

def calculate_kiwisaver(income, percent):
    return income * (percent / 100)

def calculate_student_loan(income):
    threshold = 22828
    return max(0, (income - threshold)) * 0.12

# ────────────────────────────────────────────────
# Streamlit App UI
# ────────────────────────────────────────────────

st.set_page_config(page_title="NZ Tax Calculator", page_icon="💰")

st.title("🇳🇿 NZ Salary Tax Calculator")
st.caption("Updated for 2024–2025 • Calculate your annual and monthly tax deductions in seconds.")

# User Inputs
income = st.number_input("Enter your annual income (NZD):", min_value=0, step=1000)
kiwisaver_percent = st.slider("KiwiSaver contribution (%)", 0, 10, 3)
has_student_loan = st.checkbox("I have a student loan")

# Run calculations if income > 0
if income > 0:
    # Calculations
    income_tax = calculate_nz_tax(income)
    acc_levy = calculate_acc_levy(income)
    kiwisaver = calculate_kiwisaver(income, kiwisaver_percent)
    student_loan = calculate_student_loan(income) if has_student_loan else 0

    total_deductions = income_tax + acc_levy + kiwisaver + student_loan
    annual_take_home = income - total_deductions
    monthly_take_home = annual_take_home / 12
    fortnightly_take_home = annual_take_home / 26
    monthly_deductions = total_deductions / 12

    # Results
    st.subheader("📊 Annual Breakdown")
    st.write(f"**Income Tax:** ${income_tax:,.2f}")
    st.write(f"**ACC Levy:** ${acc_levy:,.2f}")
    st.write(f"**KiwiSaver ({kiwisaver_percent}%):** ${kiwisaver:,.2f}")
    if has_student_loan:
        st.write(f"**Student Loan Repayment:** ${student_loan:,.2f}")
    
    st.markdown("---")
    st.subheader("💸 Net Take-Home Pay")
    st.write(f"**Total Annual Deductions:** ${total_deductions:,.2f}")
    st.write(f"**Monthly Deductions:** ${monthly_deductions:,.2f}")
    st.write(f"**Fortnightly Take-Home Pay:** ${fortnightly_take_home:,.2f}")
    st.write(f"**Monthly Take-Home Pay:** ${monthly_take_home:,.2f}")
