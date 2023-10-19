# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")

from decouple import config

DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT', default=3306, cast=int)
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
