-- models/staging/stg_owid_covid2.sql

{{ config(materialized='view') }}

SELECT
    iso_code,
    continent,
    location,
    date,
    total_cases,
    new_cases,
    total_deaths,
    new_deaths,
    people_vaccinated,
    people_fully_vaccinated
FROM {{ source('raw_data', 'owid_covid2') }}
