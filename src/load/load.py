from typing import List
import pandas as pd
from dotenv import load_dotenv
from utils.utils import setup_logger
import os
from sqlalchemy import create_engine, text

# this ensures .env not used when ECS runs python script
if os.getenv("RUNNING_IN_ECS") != "true":
    load_dotenv()
logger = setup_logger(__name__)


# Insert transformed forecast data into RDS using pandas and sqlalchemy
def insert_forecasts_to_db(dfs: List[pd.DataFrame]) -> None:
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    with engine.connect() as conn:
        result = conn.execute(text("SELECT City, forecast_time FROM weather_forecast"))
        existing_keys = result.fetchall()
        existing_set = set((row[0], row[1]) for row in existing_keys)
        existing_set = set(
            (city, forecast_time.replace(tzinfo=None))
            for city, forecast_time in existing_set
        )

    for df in dfs:
        df["forecast_time"] = pd.to_datetime(df["forecast_time"]).dt.tz_localize(None)
        df_filtered = df[
            ~df.apply(
                lambda row: (row["City"], row["forecast_time"]) in existing_set, axis=1
            )
        ]
        if not df_filtered.empty:
            df_filtered.to_sql(
                "weather_forecast", con=engine, if_exists="append", index=False
            )

    logger.info("Forecast data inserted into RDS via pandas.to_sql.")
