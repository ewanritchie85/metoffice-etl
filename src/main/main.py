from extract.extract import upload_multiple_cities_json
from transform.transform import transform_data_to_dataframe
from load.load import insert_forecasts_to_db
from utils.utils import setup_logger

logger = setup_logger(__name__)

def main():
    cities = ["London", "Tokyo", "New York", "Edinburgh"]

    logger.info("Starting ETL pipeline")
    
    # Extract
    logger.info("Extracting forecast data to S3")
    upload_multiple_cities_json(cities)

    # Transform
    logger.info("Transforming data from S3")
    dfs = transform_data_to_dataframe()

    # Load
    logger.info("Loading data into RDS")
    insert_forecasts_to_db(dfs)

    logger.info("ETL pipeline complete")

if __name__ == "__main__":
    main()