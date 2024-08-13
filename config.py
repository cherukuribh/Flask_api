import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'a_hard_to_guess_string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
