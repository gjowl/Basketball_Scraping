import streamlit as st
import pandas as pd
import os

# prior to running: python3.8 -m venv venv
# install required programs into venv: pip install -r requirements.txt
# to run: streamlit run site.py --server.headless true
# probably add a config to the above?

# Load data
cwd = os.getcwd()
data = pd.read_csv(f'{cwd}/example_data.csv')

# output it to the page
st.write(data)
