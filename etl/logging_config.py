import functools
import logging
import time
from logging.handlers import RotatingFileHandler


class LoggerManager:
    @staticmethod
    def get_logger(name, log_file="etl.log", level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Avoid adding handlers multiple times
        if not logger.hasHandlers():
            # Construct the absolute path relative to the script's location

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            file_handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=2
            )
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def log_execution(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            logger.info(f"Starting {func.__name__} function")
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(
                    f"Finished {func.__name__} function in {elapsed_time:.4f} seconds"  # noqa
                )

        return wrapper
