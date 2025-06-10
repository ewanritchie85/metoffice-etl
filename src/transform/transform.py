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


def transform_data_to_dataframe(bucket=None, s3_client=None) -> pd.DataFrame:

    logger.info(f"Initialising s3 client")
    s3_client, bucket = get_s3_client_and_landing_bucket(bucket, s3_client)

    # currently only working for reading one s3 object
    key = s3_client.list_objects_v2(Bucket=bucket)["Contents"][0]["Key"]
    city = key.split("/")[-1].replace(".json", "")

    logger.info(f"Retrieving S3 object: {key}")
    response = s3_client.get_object(Bucket=bucket, Key=key)

    logger.info(f"Reading {key}")
    json_data = json.loads(response["Body"].read().decode("utf-8"))

    forecasts = json_data["features"][0]["properties"]["timeSeries"]
    coordinates = json_data["features"][0]["geometry"]["coordinates"]

    df = pd.DataFrame(forecasts)
    
    df = select_wanted_columns(df)
    df.insert(0, 'City', city)
    df["Latitude"] = coordinates[1]
    df["Longitude"] = coordinates[0]
    df["Elevation"] = coordinates[2]

    
    df.to_csv('data/test_csv.csv', index=False)
    return df


# temporary main function to test transform
if __name__ == "__main__":
    transform_data_to_dataframe()
