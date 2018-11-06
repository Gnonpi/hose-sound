import os
from pathlib import Path

from dotenv import load_dotenv

APP_ENV = os.environ.get('APP_ENV', 'dev')
dot_env_path = Path(__file__).parents[1].joinpath('config/' + APP_ENV + '.env')
load_dotenv(dot_env_path)