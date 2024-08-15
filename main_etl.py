from etl.config import Config
from etl.extractors import JSONURLExtractor
from etl.loaders.facts_loader import FactsLoader
from etl.repositories.postgres_repository import PostgresRepository
from etl.transformers.fact_transformer import FactTransformer


def run_etl():
    url = Config.resource_url
    # Step 1: Extract the data
    extractor = JSONURLExtractor(url)
    raw_data = extractor.extract()

    db_uri = Config.db_uri
    repository = PostgresRepository(db_uri)

    # Step 2: Transform the data
    transformer = FactTransformer(data_repository=repository)
    transformed_data, expired_data = transformer.transform(raw_data)

    # Step 3: Load the data into PostgreSQL
    loader = FactsLoader(data_repository=repository)
    loader.load(transformed_data, expired_data)


if __name__ == "__main__":
    run_etl()
