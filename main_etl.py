from etl.config import Config
from etl.extractors import JSONURLExtractor
from etl.loaders.postgres_loader import PostgresLoader
from etl.transformers.fact_transformer import FactTransformer


def run_etl():
    url = Config.resource_url
    db_uri = Config.db_uri
    # Step 1: Extract the data
    extractor = JSONURLExtractor(url)
    raw_data = extractor.extract()

    # Step 2: Transform the data
    transformer = FactTransformer()
    transformed_data = transformer.transform(raw_data)

    # Step 3: Load the data into PostgreSQL
    loader = PostgresLoader(db_uri)
    loader.load(transformed_data)


if __name__ == "__main__":
    run_etl()
