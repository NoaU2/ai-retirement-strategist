import streamlit as st
import pandas as pd
import altair as alt

def simulate_retirement(current_age, retirement_age, total_compensation, cost_of_living, annual_return=0.07, initial_portfolio=0):
    """
    Simulate the growth of a retirement portfolio with annual contributions.
    """
    annual_savings = total_compensation - cost_of_living
    ages = list(range(current_age, retirement_age + 1))
    portfolio_values = []
    portfolio = initial_portfolio

    for age in ages:
        portfolio += annual_savings
        portfolio *= (1 + annual_return)
        portfolio_values.append(portfolio)
    
    return ages, portfolio_values

def main():
    st.title("Interactive Retirement Calculator")

    # Sidebar inputs for real-time adjustments
    st.sidebar.header("Input Parameters")
    current_age = st.sidebar.number_input("Current Age", min_value=0, max_value=120, value=30, step=1)
    retirement_age = st.sidebar.number_input("Target Retirement Age", min_value=current_age+1, max_value=120, value=65, step=1)
    total_compensation = st.sidebar.number_input("Total Annual Compensation ($)", min_value=0.0, value=80000.0, step=1000.0, format="%.2f")
    cost_of_living = st.sidebar.number_input("Annual Cost of Living ($)", min_value=0.0, value=50000.0, step=1000.0, format="%.2f")
    goal_amount = st.sidebar.number_input("Retirement Goal Amount ($)", min_value=0.0, value=1000000.0, step=10000.0, format="%.2f")
    annual_return = st.sidebar.slider("Expected Annual Return Rate (%)", min_value=0.0, max_value=15.0, value=7.0, step=0.1) / 100.0

    # Run simulation
    ages, portfolio_values = simulate_retirement(current_age, retirement_age, total_compensation, cost_of_living, annual_return)
    final_amount = portfolio_values[-1]
    withdrawal_amount = final_amount * 0.04  # using the 4% rule

    # Display results
    st.header("Retirement Projections")
    annual_savings = total_compensation - cost_of_living
    st.write(f"You are investing **${annual_savings:,.2f}** per year.")
    st.write(f"At age **{retirement_age}**, your portfolio is projected to be worth **${final_amount:,.2f}** (Total Compensation - Cost of Living)")
    st.write(f"Following the 4% rule, you could withdraw approximately **${withdrawal_amount:,.2f}** per year in retirement.")

    # Prepare data for interactive chart
    data = pd.DataFrame({
        "Age": ages,
        "Portfolio Value": portfolio_values
    })

    # Create interactive line chart with Altair
    line_chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("Age:Q"),
        y=alt.Y("Portfolio Value:Q", title="Portfolio Value ($)")
    ).properties(
        width=700,
        height=400,
        title="Portfolio Growth Over Time"
    )

    # Add a rule (dashed line) for the retirement goal
    rule = alt.Chart(pd.DataFrame({'Goal': [goal_amount]})).mark_rule(color='red', strokeDash=[5,5]).encode(
        y=alt.Y('Goal:Q')
    )

    st.altair_chart(line_chart + rule, use_container_width=True)

if __name__ == "__main__":
    main()
