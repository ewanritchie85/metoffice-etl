import json
import dotenv
import pandas as pd
from utils.utils import (
    get_s3_client_and_landing_bucket,
    select_wanted_columns,
    setup_logger,
)

logger = setup_logger(__name__)

dotenv.load_dotenv()

# S3 processed keys tracking
PROCESSED_KEYS_PATH = "processed/processed_keys.txt"

def load_processed_keys_from_s3(s3_client=None, bucket=None) -> set:
    s3_client, bucket = get_s3_client_and_landing_bucket(bucket, s3_client)
    logger.info("Getting processed keys from S3")
    try:
        response = s3_client.get_object(Bucket=bucket, Key=PROCESSED_KEYS_PATH)
        return set(response["Body"].read().decode("utf-8").splitlines())
    except s3_client.exceptions.NoSuchKey:
        return set()

def save_processed_keys_to_s3(keys: list, s3_client=None, bucket=None) -> None:
    s3_client, bucket = get_s3_client_and_landing_bucket(bucket, s3_client)
    logger.info("Saving processed keys to S3")
    body = "\n".join(keys).encode("utf-8")
    s3_client.put_object(Bucket=bucket, Key=PROCESSED_KEYS_PATH, Body=body)


def transform_data_to_dataframe(bucket=None, s3_client=None) -> list:
    logger.info(f"Initialising s3 client")
    s3_client, bucket = get_s3_client_and_landing_bucket(bucket, s3_client)
    dfs = []
    processed_keys = load_processed_keys_from_s3()
    newly_processed = []

    bucket_objects = s3_client.list_objects_v2(Bucket=bucket)['Contents']
    for object in bucket_objects:
        key = object['Key']
        if not key or not key.endswith('.json') or key in processed_keys:
            continue
        try:
            city = key.split('/')[-1].replace('.json', '')
            logger.info(f"Retrieving S3 object: {key}")
            response = s3_client.get_object(Bucket=bucket, Key=key)

            logger.info(f"Reading {key}")
            json_data = json.loads(response["Body"].read().decode("utf-8"))

            forecasts = json_data["features"][0]["properties"]["timeSeries"]
            coordinates = json_data["features"][0]["geometry"]["coordinates"]

            df = pd.DataFrame(forecasts)
            df = select_wanted_columns(df)
            df.insert(0, "City", city)
            df["Latitude"] = coordinates[1]
            df["Longitude"] = coordinates[0]
            df["Elevation"] = coordinates[2]
            df = rename_columns(df)
            df["forecast_time"] = pd.to_datetime(df["forecast_time"]).dt.tz_localize(None)
            dfs.append(df)
            newly_processed.append(key)
        except (KeyError, json.JSONDecodeError) as e:
            logger.warning(f"skipping {key} due to: {e}")
            continue

    if newly_processed:
        all_keys = list(processed_keys.union(newly_processed))
        save_processed_keys_to_s3(all_keys)

    return dfs


# Matches columns with db schema
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "time": "forecast_time",
        "daySignificantWeatherCode": "weather_code",
        "dayMaxScreenTemperature": "max_temp",
        "nightMinScreenTemperature": "min_temp",
        "midday10MWindSpeed": "midday_wind_speed",
        "midday10MWindDirection": "midday_wind_dir",
        "midnight10MWindSpeed": "midnight_wind_speed",
        "midnight10MWindDirection": "midnight_wind_dir",
        "middayRelativeHumidity": "midday_humidity",
        "midnightRelativeHumidity": "midnight_humidity",
        "dayProbabilityOfRain": "rain_prob"
    })
