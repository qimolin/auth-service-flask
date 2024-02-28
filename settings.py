import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

PRIVATE_KEY_PASSWORD = os.getenv("PRIVATE_KEY_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")