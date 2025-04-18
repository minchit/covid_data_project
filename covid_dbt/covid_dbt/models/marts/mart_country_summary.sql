-- models/marts/mart_country_summary.sql

{{ config(materialized='table') }}

SELECT
    location,
    MAX(date) AS latest_date,
    MAX(total_cases) AS total_cases,
    MAX(total_deaths) AS total_deaths,
    MAX(people_fully_vaccinated) AS people_fully_vaccinated
FROM {{ ref('stg_owid_covid2') }}
GROUP BY location
