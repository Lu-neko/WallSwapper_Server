import os
from dotenv import load_dotenv

load_dotenv()

DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URL = os.getenv("DB_URL")