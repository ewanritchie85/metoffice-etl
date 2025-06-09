
# Met Office ETL Project

## ETL Flow Overview

This project performs an Extract-Transform-Load (ETL) workflow to collect weather forecast data from the Met Office API and store it in an S3 bucket.

### 1. Infrastructure Setup

- **Terraform** is used to provision:
  - Backend configuration and state management (via HCL)
  - An S3 landing bucket

### 2. Data Extraction

- A **FastAPI** app is used to issue `GET` requests to the Met Office Global Spot Forecast API.
- The function `get_data_from_api` calls the API using:
  - `city` name
  - `span` (`daily`, `hourly` or `three-hourly`; default: `daily`)

### 3. Data Upload

- The function `upload_json_to_landing_s3`:
  - Uses `boto3` to upload raw GeoJSON forecast data to the landing S3 bucket.
  - Stores the data in the following format:
    ```
    s3://<bucket-name>/<city>/<YYYY>/<MM>/<DD>/<HH-MM>.json
    ```

---
