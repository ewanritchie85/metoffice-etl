import os
from typing import cast
import pymysql
from dotenv import load_dotenv
from utils.utils import setup_logger

logger = setup_logger(__name__)
load_dotenv()


def db_connection():
    try:
        conn = pymysql.connect(
            host=cast(str, os.getenv("DB_ENDPOINT")),
            user=cast(str, os.getenv("DB_USER_NAME")),
            password=cast(str, os.getenv("DB_PASSWORD")),
            database=cast(str, os.getenv("DB_NAME")),
            port=int(os.getenv("DB_PORT", "3306")),
        )
        return conn
    except pymysql.MySQLError as e:
        logger.error(f"Failed to make connection to DB: {e}")
        raise


def create_db_table() -> None:
    logger.info("making DB connection")
    conn = db_connection()
    logger.info("Creating DB Table")
    with conn.cursor() as cursor:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            forecast_time DATETIME NOT NULL,

            weather_code FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            midday_wind_speed FLOAT,
            midday_wind_dir FLOAT,
            midnight_wind_speed FLOAT,
            midnight_wind_dir FLOAT,
            midday_humidity FLOAT,
            midnight_humidity FLOAT,
            rain_prob FLOAT,

            latitude FLOAT,
            longitude FLOAT,
            elevation FLOAT,

            UNIQUE KEY unique_city_time (city, forecast_time)
        )
    """
        )
    conn.commit()
    logger.info("Table created successfully")
    conn.close()
    return

def drop_db_table():
    conn = db_connection()
    logger.info("Clearing DB table")
    with conn.cursor() as cursor:
        cursor.execute(
            "DROP TABLE weather_forecast"
        )
    conn.commit()
    logger.info("Table dropped successfully")
    conn.close()
