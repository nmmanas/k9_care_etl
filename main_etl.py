# main_etl.py

from etl.extract import extract_data
from etl.load import load_data
from etl.transform import transform_data


def run_etl():
    # Step 1: Extract the data
    data = extract_data()

    # Step 2: Transform the data
    transformed_data = transform_data(data)

    # Step 3: Load the data into PostgreSQL
    load_data(transformed_data)


if __name__ == "__main__":
    run_etl()
