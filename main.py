import pandas as pd
import streamlit as st

# Function to generate the amortization table
def amortization_table(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    no_of_payments = years * 12
    monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -no_of_payments)
    total_payment = monthly_payment * no_of_payments
    total_interest = total_payment - principal

    schedule = []
    balance = principal

    for month in range(1, no_of_payments + 1):
        beginning_balance = balance
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append([
            month,
            round(beginning_balance, 2),
            round(monthly_payment, 2),
            round(interest, 2),
            round(principal_payment, 2),
            round(max(0, balance), 2)
        ])

    columns = ['Month', 'Beginning Balance', 'Payment', 'Interest', 'Principal Payment', 'Remaining Balance']
    return pd.DataFrame(schedule, columns=columns), round(monthly_payment, 2), round(total_payment, 2), round(total_interest, 2), no_of_payments

# Main app function
def main():
    st.title("Amortization Table Calculator")

    # User Inputs
    principal = st.number_input("Loan Amount", min_value=0.0)
    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=1)
    years = st.number_input("Loan Term (Years)", min_value=1)
    currency_symbol = st.text_input("Currency Symbol", value="$")

    if st.button("Calculate Amortization Table"):
        # Generate table and calculations
        Amortization_Table, monthly_payment, total_payment, total_interest, no_of_payments = amortization_table(principal, annual_rate, years)

        st.subheader("Loan Summary")
        st.write(f"**Number of Payments:** {no_of_payments}")
        st.write(f"**Monthly Rate:** {annual_rate / 12:.2f}%")
        st.write(f"**Loan Amount:** {currency_symbol}{principal}")
        st.write(f"**Monthly Payment:** {currency_symbol}{monthly_payment:,.2f}")
        st.write(f"**Total Payment:** {currency_symbol}{total_payment:,.2f}")
        st.write(f"**Total Interest:** {currency_symbol}{total_interest:,.2f}")

        # Display detailed amortization table
        st.subheader("Amortization Table")
        # Convert the DataFrame to an HTML table without the index
        st.write(Amortization_Table.to_html(index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

