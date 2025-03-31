import streamlit as st

# ───────────────────────────────────────────────
# NZ Tax Functions
# ───────────────────────────────────────────────

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

# ───────────────────────────────────────────────
# India Tax Functions
# ───────────────────────────────────────────────

def india_old_regime_tax(income, deductions):
    taxable_income = max(0, income - deductions)
    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 250000 * 0.05 + (taxable_income - 500000) * 0.20
    else:
        tax = 250000 * 0.05 + 500000 * 0.20 + (taxable_income - 1000000) * 0.30
    return tax

def india_new_regime_tax(income):
    slabs = [(300000, 0), (600000, 0.05), (900000, 0.10),
             (1200000, 0.15), (1500000, 0.20), (float('inf'), 0.30)]
    tax = 0
    prev_limit = 0
    for limit, rate in slabs:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break
    return tax

# ───────────────────────────────────────────────
# Streamlit UI
# ───────────────────────────────────────────────

st.set_page_config(page_title="Global Tax Calculator", page_icon="🌍")
st.title("🌍 Global Salary Tax Calculator")
st.caption("Compare take-home pay for India 🇮🇳 and New Zealand 🇳🇿 (2024–25)")

# Country selection
country = st.selectbox("Select your country:", ["New Zealand", "India"])

income = st.number_input("Enter your annual income:", min_value=0, step=1000)

# NZ Logic
if country == "New Zealand":
    kiwisaver_percent = st.slider("KiwiSaver contribution (%)", 0, 10, 3)
    has_student_loan = st.checkbox("I have a student loan")

    if income > 0:
        income_tax = calculate_nz_tax(income)
        acc_levy = calculate_acc_levy(income)
        kiwisaver = calculate_kiwisaver(income, kiwisaver_percent)
        student_loan = calculate_student_loan(income) if has_student_loan else 0

        total_deductions = income_tax + acc_levy + kiwisaver + student_loan
        annual_take_home = income - total_deductions
        monthly_take_home = annual_take_home / 12
        fortnightly_take_home = annual_take_home / 26

        st.subheader("📊 NZ Annual Breakdown")
        st.write(f"**Income Tax:** ${income_tax:,.2f}")
        st.write(f"**ACC Levy:** ${acc_levy:,.2f}")
        st.write(f"**KiwiSaver ({kiwisaver_percent}%):** ${kiwisaver:,.2f}")
        if has_student_loan:
            st.write(f"**Student Loan Repayment:** ${student_loan:,.2f}")
        st.markdown("---")
        st.write(f"**Annual Take-Home Pay:** ${annual_take_home:,.2f}")
        st.write(f"**Monthly Take-Home Pay:** ${monthly_take_home:,.2f}")
        st.write(f"**Fortnightly Take-Home Pay:** ${fortnightly_take_home:,.2f}")

# India Logic
else:
    regime = st.radio("Select tax regime:", ["Old Regime", "New Regime"])

    if regime == "Old Regime":
        # User-defined deductions
        ded_80c = st.number_input("80C (LIC, ELSS, PF, etc.)", 0, 150000, step=5000)
        ded_80d = st.number_input("80D (Medical Insurance)", 0, 50000, step=5000)
        standard_ded = 50000  # fixed
        hra = st.number_input("House Rent Allowance (HRA)", 0, 200000, step=5000)
        total_deductions = min(ded_80c, 150000) + min(ded_80d, 50000) + standard_ded + hra
        income_tax = india_old_regime_tax(income, total_deductions)

    else:  # New Regime
        income_tax = india_new_regime_tax(income)
        total_deductions = 0

    annual_take_home = income - income_tax
    monthly_take_home = annual_take_home / 12
    st.subheader("📊 India Tax Breakdown")
    if regime == "Old Regime":
        st.write(f"**Total Deductions:** ₹{total_deductions:,.0f}")
    st.write(f"**Income Tax:** ₹{income_tax:,.0f}")
    st.markdown("---")
    st.write(f"**Annual Take-Home Pay:** ₹{annual_take_home:,.0f}")
    st.write(f"**Monthly Take-Home Pay:** ₹{monthly_take_home:,.0f}")
