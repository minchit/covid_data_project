import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

# Streamlit UI
st.set_page_config(page_title="Global COVID-19 Dashboard", layout="wide")
st.title("🌍 Global COVID-19 Dashboard")

# Get distinct country list
@st.cache_data
def get_countries():
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT location FROM owid_covid2 ORDER BY location")
    return [row[0] for row in cur.fetchall()]

country = st.selectbox("Select a Country", get_countries())

# Fetch data
@st.cache_data
def load_data(selected_country):
    query = f"""
        SELECT date, new_cases, total_deaths, people_fully_vaccinated
        FROM owid_covid2
        WHERE location = %s
        ORDER BY date
    """
    cur = conn.cursor()
    cur.execute(query, (selected_country,))
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=cols)

df = load_data(country)
df['DATE'] = pd.to_datetime(df['DATE'])  # Ensure date is datetime format


# 📅 Date Range Filter
st.subheader("📅 Filter by Date Range")
min_date = df['DATE'].min()
max_date = df['DATE'].max()

start_date, end_date = st.date_input(
    "Select date range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Apply date filter
df = df[(df['DATE'] >= pd.to_datetime(start_date)) & (df['DATE'] <= pd.to_datetime(end_date))]

# 🧮 Summary KPIs
st.markdown("## 🧮 Summary KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("🦠 Total New Cases", f"{df['NEW_CASES'].sum():,.0f}")
col2.metric("💀 Max Total Deaths", f"{df['TOTAL_DEATHS'].max():,.0f}")
try:
    vax_ratio = (
        df['PEOPLE_FULLY_VACCINATED'].dropna().max() / df['NEW_CASES'].sum()
    ) * 100 if df['NEW_CASES'].sum() > 0 else 0
    col3.metric("💉 % Vaccinated", f"{vax_ratio:.2f}%")
except:
    col3.metric("💉 % Vaccinated", "N/A")

# Charts
st.subheader(f"📈 New Cases in {country}")
fig_cases = px.line(df, x="DATE", y="NEW_CASES", labels={"NEW_CASES": "New Cases"})
st.plotly_chart(fig_cases, use_container_width=True)

st.subheader(f"💀 Total Deaths in {country}")
fig_deaths = px.line(df, x="DATE", y="TOTAL_DEATHS", labels={"TOTAL_DEATHS": "Total Deaths"})
st.plotly_chart(fig_deaths, use_container_width=True)

st.subheader(f"💉 Vaccinations in {country}")
fig_vax = px.line(df, x="DATE", y="PEOPLE_FULLY_VACCINATED", labels={"PEOPLE_FULLY_VACCINATED": "Fully Vaccinated"})
st.plotly_chart(fig_vax, use_container_width=True)