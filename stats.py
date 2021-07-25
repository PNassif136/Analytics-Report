# Import libraries
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

# Configure default page settings to wide (not centered)
st.set_page_config(layout="wide")

# Link Google sheet as a data source
sheet_id = "1qxZ0uzz1Z0WUKdzaEaDg46wonsdD41ZqjZrE8cb1mGU"
sheet_name = "Leads"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Create a title
st.header('Analytics Report (Prototype)')

# Password-Protect the app and specify scenarios
password = st.sidebar.text_input("Enter Password", type="password", key="1")

if password == 'coffee':
    # Load the dataset into a dataframe & greet user
    df = pd.read_csv(url)
    st.success('Welcome to the Interactive Dashboard!')

elif password != 'coffee':
    # Deny access & stop all subsequent codes from executing
    st.warning('Access Denied - Enter Correct Password')
    st.stop()

# Create selectbox to choose appropriate section
option = st.sidebar.radio('What would you like to do?',
                ('Facebook & Website Leads', 'Campaign Analytics'), key="3")

# Remove unnecessary columns
df = df.drop(['Timestamp'], axis=1)

# Convert 'Date Collected' column to datetime, then sort by descending order
df["Date"] = pd.to_datetime(df["Date Collected"]).dt.date
df = df.sort_values(by="Date", ascending=False)

# Rename columns
df.rename(columns={'Total Number of Prospects':'# Prospects',
                    'Total Number of Maids':'# Maids',
                    '# of Filipina':'# Filipina',
                    '# of N/A':'# N/A',
                    '# of Africans':'# Africans',
                    '# of Other Nationalities':'# Others'
                    }, inplace=True)

## Facebook & Website Leads
if option == "Facebook & Website Leads":     #If this section is selected

    # Display the number of rows and columns in a sentence
    st.write("This dataset has: ", df.shape[0], " records and ", df.shape[1], " features")

    # Add a slider that filters total number of records and updates all subsequent values
    records = st.sidebar.slider('Select total desired records', df.shape[0], 1, df.shape[0], key="2")
    df = df.iloc[0:records]

    # Display df.head() under an expandable tab
    with st.beta_expander("Daily Records"):
        # Reindex the table  so that the date comes first
        df = df.reindex(columns=['Date', '# Prospects', '# Maids', '# Filipina',
                                '# N/A', '# Africans', '# Others'])
        st.write(df.head(records))

        # Option to download as csv
        if st.button('Download CSV', key="4"):
            df.to_csv('daily_records.csv', index=False)

    # Review the summary statistics under an expandable tab
    with st.beta_expander("Summary Statistics"):
        summary = df.describe().round().loc[['mean','min','max']]
        st.write(summary)

        # Option to download as csv
        if st.button('Download CSV', key="5"):
            summary.to_csv('summary_stats.csv', index=False)

    # Visual Analysis
    with st.beta_container():                      #Creates a container/box of graphs so they look like a dashboard
        col1, col2= st.beta_columns([1,1])         #Creates 2 side-by-side graphs of equal sizes

        # Line Chart – Prospect Numbers Collected over Time
        with col1:
            fig1 = px.line(df, x="Date", y="# Prospects",
                      title = "Prospect Numbers Collected over Time")
            fig1.layout.update(height=450, width=450, xaxis_title='Date', yaxis_title='# Prospects',
                                xaxis_showgrid=False, yaxis_showgrid=False)
            st.write(fig1)

        # Line Chart – Maid Numbers Collected over Time
        with col2:
            fig2 = px.line(df, x="Date", y="# Maids",
                      title = "Maid Numbers Collected over Time")
            fig2.layout.update(height=450, width=450, xaxis_title='Date', yaxis_title='# Maids',
                                xaxis_showgrid=False, yaxis_showgrid=False)
            st.write(fig2)
