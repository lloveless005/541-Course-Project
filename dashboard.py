import streamlit as st
from main import *

st.title("Loan Risk Dashboard")

riskTolerance = st.number_input("Risk Tolerance %", min_value = 0.0, max_value = 100.0)

RR = st.number_input("Recovery Rate %", min_value = 0.0, max_value = 100.0)

loanLife = st.number_input("Loan Term (years)", min_value = 1, max_value = 100)

sims = st.number_input("Simulations", min_value = 1, max_value = 1_000_000)