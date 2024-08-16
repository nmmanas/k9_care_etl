from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.config import Config
from etl.error_reporting import ErrorReporter
from etl.extractors import JSONURLExtractor
from etl.loaders.facts_loader import FactsLoader
from etl.logging_config import LoggerManager
from etl.repositories.postgres_repository import PostgresRepository
from etl.transformers.fact_transformer import FactTransformer

# get logging
logging = LoggerManager.get_logger(__name__)

# Initialize the ErrorReporter with console output enabled
error_reporter = ErrorReporter(logging, enable_console=True)


url = Config.resource_url
db_uri = Config.db_uri

repository = PostgresRepository(db_uri)


def etl_extract(**kwargs):
    try:
        extractor = JSONURLExtractor(url)
        raw_data = extractor.extract()
        return raw_data
    except Exception as e:
        error_reporter.report_error(f"Extraction error: {e}")
        raise e


def etl_transform(**kwargs):
    try:
        raw_data = kwargs["ti"].xcom_pull(task_ids="extract")
        transformer = FactTransformer(data_repository=repository)
        transformed_data, expired_data = transformer.transform(raw_data)
        return transformed_data, expired_data
    except Exception as e:
        error_reporter.report_error(f"Transformation error: {e}")
        raise e


def etl_load(**kwargs):
    try:
        transformed_data, expired_data = kwargs["ti"].xcom_pull(
            task_ids="transform"
        )
        loader = FactsLoader(data_repository=repository)
        loader.load(transformed_data, expired_data)
    except Exception as e:
        error_reporter.report_error(f"Loading error: {e}")
        raise e


def send_summary_report(**kwargs):
    error_reporter.send_summary_report()


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 16),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

with DAG(
    "etl_pipeline",
    default_args=default_args,
    description="An ETL pipeline DAG with summary reporting",
    schedule_interval="@daily",
    catchup=False,
    template_searchpath="/opt/airflow/etl",
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=etl_extract,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=etl_transform,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=etl_load,
    )

    summary_task = PythonOperator(
        task_id="summary_task",
        python_callable=send_summary_report,
    )

    extract >> transform >> load >> summary_task
