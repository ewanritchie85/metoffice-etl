import csv
import boto3
import os


def get_lat_long_from_city(city: str) -> tuple:
    """
    Get latitude and longitude from a city name.

    Args:
        city (str): The name of the city.

    Returns:
        tuple: A tuple containing latitude and longitude.
    """
    with open("data/world-cities.csv", mode="r", encoding="utf-8") as file:

        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row["city"].strip().lower() == city.strip().lower():
                lat_long = (float(row["latitude"]), float(row["longitude"]))
                break
        else:
            raise ValueError(f"'{city}' not found in the dataset.")

    return lat_long


def get_s3_client_and_bucket(bucket=None, s3_client=None):
    """provides an S3 client and bucket name.

    Args:
        bucket: Bucket name. Defaults to None as it is fetched 
                from environment variable if not provided.
        s3_client : Defaults to None and is created if not provided.

    Returns:
        boto3 S3 client and bucket name(str).
    """
    if not s3_client:
        s3_client = boto3.client("s3")
    if not bucket:
        bucket = os.getenv("LANDING_BUCKET_NAME")
    return s3_client, bucket
