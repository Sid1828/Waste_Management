#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Load data (adapt the path or use st.file_uploader)
@st.cache_data
def load_data():
    path = r"C:\Users\SIDDHARTH EKBOTE\Downloads\Final Waste Management Data (1).xlsx"
    df = pd.read_excel(path)
    return df

df = load_data()

st.title("Waste Management Dashboard")
st.write("Interactive visualizations for the Final Waste Management dataset.")

st.subheader("Raw data preview")
st.dataframe(df.head())

# Sidebar filters – adapt column names you actually use
st.sidebar.header("Filters")
year_col = "refYear"
flow_col = "flowCode"         # e.g. import / export
country_col = "reporterDesc"  # Germany, etc.

years = sorted(df[year_col].dropna().unique())
flows = sorted(df[flow_col].dropna().unique())
countries = sorted(df[country_col].dropna().unique())

selected_year = st.sidebar.selectbox("Year", years)
selected_flow = st.sidebar.selectbox("Flow", flows)
selected_country = st.sidebar.selectbox("Reporter", countries)

filtered = df[
    (df[year_col] == selected_year) &
    (df[flow_col] == selected_flow) &
    (df[country_col] == selected_country)
]

st.subheader("Filtered data")
st.dataframe(filtered.head())


# In[ ]:




