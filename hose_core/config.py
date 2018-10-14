import os
from pathlib import Path
from dotenv import load_dotenv

APP_ENV = os.environ.get('APP_ENV', 'dev')
dot_env_path = Path(__file__).parents[1].joinpath('config/' + APP_ENV + '.env')
load_dotenv(dot_env_path)

DSN_DB = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DBNAME'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
}
POSTGRES_DSN = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(**DSN_DB)

