import streamlit as st
import matplotlib.pyplot as plt
from main import *

st.title("Loan Risk Dashboard")

left_column, right_column = st.columns(2)

with left_column:
    investment = st.number_input("Investment per Company ($)", min_value = 1)

    RR = st.number_input("Recovery Rate (%)", min_value = 0.0, max_value = 100.0)

with right_column:
    loanLife = st.number_input("Loan Term (years)", min_value = 1, max_value = 100)

    sims = st.number_input("Simulations", min_value = 1, max_value = 10_000_000)

if st.button(label = 'Run Simulations'):
    startTime = time.perf_counter()

    bals = []
    losses = []
    risks = []
    index = 0
    riskTolerance = 5

    while riskTolerance <= 100:
        risks.append(riskTolerance)

        myBal, totalLosses = riskSim(yearmat_a, riskTolerance/100, RR/100, loanLife, sims, investment)

        bals.append(myBal)
        losses.append(totalLosses)

        index += 1
        riskTolerance += 5

    endTime = time.perf_counter()
    elapsed = endTime - startTime   

    bals = np.array(bals)
    losses = np.array(losses)
    risks = np.array(risks)

    balsGraph, ax1 = plt.subplots()

    ax1.plot(risks, bals)
    ax1.axhline(y = sims * investment * (1.03442) ** loanLife, color = "red", linestyle = "dashed")
    ax1.set_xlabel("Risk Tolerance (%)")
    ax1.set_ylabel("Final Balance ($)")
    ax1.set_title("Final Balance By Risk Tolerance")

    lossesGraph, ax2 = plt.subplots()

    ax2.plot(risks, losses)
    ax2.set_xlabel("Risk Tolerance (%)")
    ax2.set_ylabel("Total Losses ($)")
    ax2.set_title("Total Losses By Risk Tolerance")

    leftGraph, rightGraph = st.columns(2)

    with leftGraph:
        st.pyplot(balsGraph)

    with rightGraph:
        st.pyplot(lossesGraph)

    st.write(f"\nTotal initial investment of \\${sims*investment:,.0f}.")
    st.write("For risk tolerance of 100%:")
    st.write(f"We now have \\${myBal:,.2f} and lost \\${totalLosses:,.2f} on defaults.")

    rfr = sims * investment * (1.03442 ** loanLife)
    profit = myBal - rfr

    totalPct = (myBal / (sims * investment)) * 100
    annualPct = ((totalPct/100)**(1 / loanLife) - 1) * 100

    st.write(f"We profited \\${profit:,.2f} over the risk-free rate of \\${rfr:,.2f}.")
    st.write(f"We got a total profit of {totalPct:.2f}%.")
    st.write(f"Yearly profit of {annualPct:.2f}%.")
    st.write(f"Program took {elapsed:.4f} seconds to run.\n")