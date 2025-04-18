# 🌍 COVID-19 Data Pipeline Project

A complete end-to-end data pipeline and dashboard project built with:

- **Snowflake** for data warehousing
- **dbt** for transformation and modeling
- **Streamlit** for interactive data visualization

---

## 📦 Project Overview

This project ingests the [Our World in Data - COVID-19 dataset](https://covid.ourworldindata.org/) into Snowflake, transforms it using dbt, and visualizes trends through an interactive Streamlit dashboard.

---

## 📊 Streamlit Dashboard

### 🔧 Features
- Country selector
- Date range filter
- KPIs (Total Cases, Deaths, Vaccination %)
- Line charts for cases, deaths, and vaccinations

### 🚀 Run Locally

```bash
cd streamlit_dashboard
pip install -r requirements.txt
streamlit run app.py
