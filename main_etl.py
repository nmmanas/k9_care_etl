from dags.etl.config import Config
from dags.etl.error_reporting import ErrorReporter
from dags.etl.extractors import JSONURLExtractor
from dags.etl.loaders.facts_loader import FactsLoader
from dags.etl.logging_config import LoggerManager
from dags.etl.repositories.postgres_repository import PostgresRepository
from dags.etl.transformers.fact_transformer import FactTransformer

# get logging
logging = LoggerManager.get_logger(__name__)

# Initialize the ErrorReporter with console output enabled
error_reporter = ErrorReporter(logging, enable_console=True)


def run_etl():
    try:
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
        pass
    except Exception as e:
        error_reporter.report_error(str(e))
    finally:
        # Send the summary report at the end of the pipeline
        error_reporter.send_summary_report()


if __name__ == "__main__":
    run_etl()
