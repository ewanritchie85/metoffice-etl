
# Met Office ETL Project

## Pre-requisites
metoffice global spot API key
Terraform Cloud account with org and workspace created
AWS credentials - stored in Terraform Cloud as env variables


## ETL Flow Overview

This project performs an Extract-Transform-Load (ETL) workflow to collect weather forecast data from the Met Office API and store it in an S3 bucket.

### 1. Infrastructure Setup

- **Terraform** is used to provision:
  - Backend configuration and state management (via HCL)
  - An S3 landing bucket
  - An RDS instance for loading clean data for analysis

### 2. Data Extraction

- A **FastAPI** app is used to issue `GET` requests to the Met Office Global Spot Forecast API.
- The function `get_data_from_api` calls the API using:
  - `city` name
  - `span` (`hourly` , `three-hourly`, default: `daily`)

### 3. Data Upload

- The function `upload_json_to_landing_s3`:
  - Uses `boto3` to upload raw GeoJSON forecast data to the landing S3 bucket.
  - Stores the data in the following format:
    ```
    s3://<bucket-name>/<YYYY-MM-DD-HH:MM>/<city>.json
    ```
### 4. Data Transformation

- The function `transform_data_to_dataframe`:
  - Retrieves **only new** forecast JSON files from the landing S3 bucket (tracked using `processed_keys.txt` in S3).
  - Extracts the weather data from the GeoJSON structure.
  - Flattens the nested structure into a clean `pandas.DataFrame`.
  - Selects desired fields and adds `city`, `longitude`, `latitude`, and `elevation`.
  - Renames dataframe columns to match DB schema.
  - Returns a list of clean dataframes.

### 5. Cleaned Data DB Loading

- SQLAlchemy and pandas upload cleaned dataframes to RDS instance.
- The loader compares forecast `City` and `forecast_time` values against existing entries and **only inserts new records**, avoiding duplicates based on a unique constraint in the database.
---
