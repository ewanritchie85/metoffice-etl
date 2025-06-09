from pprint import pprint
import logging
import json
import dotenv
import pandas as pd
from utils.utils import get_s3_client_and_bucket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
# Load environment variables from .env file
dotenv.load_dotenv()


# json arg to be added in due course
def transform_data_to_dataframe(bucket=None, s3_client=None) -> pd.DataFrame:

    s3_client, bucket = get_s3_client_and_bucket(bucket, s3_client)
    
    key = "2025/06/09/11/London.json"
      
    response = s3_client.get_object(
        Bucket=bucket,
        Key=key
            )
    json_data = json.loads(response["Body"].read().decode("utf-8"))

    city = "london"
    forecast = json_data["features"][0]["properties"]["timeSeries"]
    coordinates = json_data["features"][0]["geometry"]["coordinates"]

    df = pd.DataFrame(forecast)
    df["city"] = city
    df["longitude"] = coordinates[0]
    df["latitude"] = coordinates[1]
    df["elevation"] = coordinates[2]

    pprint(df.head())
    return df


# temporary main function to test transform
if __name__ == "__main__":
    transform_data_to_dataframe()
