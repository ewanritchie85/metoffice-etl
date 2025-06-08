import csv


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
