import json
import os
from dotenv import load_dotenv

import pandas as pd
import streamlit as st

from app_sections import (overview_grid, donors_section, about, at_risk_projects, implementation)

import streamlit as st
from multiapp import MultiApp

import boto3

load_dotenv()

app = MultiApp()

st.sidebar.markdown("## Navigation")
# Add all your application here
app.add_app("About the Dashboard", about.app)


app.add_app("Monthly Report: Metrics", overview_grid.app)
app.add_app("Analysis: Donor Behavior", donors_section.app)

app.add_app("Marketing Tool: Expiring Projects", at_risk_projects.app)



# app.add_app("The Data Set", dataset.app)
app.add_app("Dashboard Implementation", implementation.app)

# The main app
st.title("DonorsChoose Dashboard")

app.run()
