from typing import List
import pandas as pd
from dotenv import load_dotenv
from utils.utils import setup_logger
import os
from sqlalchemy import create_engine

load_dotenv()
logger = setup_logger(__name__)

# Insert transformed forecast data into RDS using pandas and sqlalchemy
def insert_forecasts_to_db(dfs: List[pd.DataFrame]) -> None:
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER_NAME')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_ENDPOINT')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    for df in dfs:
        df.to_sql("weather_forecast", con=engine, if_exists="append", index=False)
    logger.info("Forecast data inserted into RDS via pandas.to_sql.")