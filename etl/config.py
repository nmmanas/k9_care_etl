import os

from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__))
ENVIRONMENTS = {
    "dev": os.path.join("..", ".env.dev"),
    "docker": os.path.join("..", ".env.docker"),
}
ENV = os.getenv("ENV") or "dev"

dotenv_path = os.path.join(
    APP_ROOT, ENVIRONMENTS.get(ENV) or os.path.join("..", ".env.dev")
)

print(f"{dotenv_path=}")

# Load Environment variables
load_dotenv(dotenv_path)


class Config:
    resource_url = "https://raw.githubusercontent.com/vetstoria/random-k9-etl/main/source_data.json"  # noqa
    db_uri = os.getenv("DB_URI")
