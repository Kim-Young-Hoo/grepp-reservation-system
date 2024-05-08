import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM')
JWT_COOKIE_KEY = os.getenv('JWT_COOKIE_KEY')
