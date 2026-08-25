
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title
st.set_page_config(page_title="Restaurant Intelligence Dashboard", layout="wide")

st.title("🍽️ Restaurant Intelligence Dashboard")
st.write("Welcome to my Restaurant Intelligence Project")

# Load dataset
df = pd.read_csv("data/cleaned_uber_eats_data (1)123.csv")

# Display dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Display dataset size
st.subheader("Dataset Shape")
st.write(df.shape)

# Display column names
st.subheader("Columns")
st.write(df.columns.tolist())

# Display summary
st.subheader("Summary Statistics")
st.write(df.describe())
