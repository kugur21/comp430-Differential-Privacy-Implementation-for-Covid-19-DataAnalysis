"""
Application settings and configuration.
Loads environment variables and provides configuration dictionaries for different parts of the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import logging.config


# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'covid_data'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'raise_on_warnings': True,
    'connection_timeout': int(os.getenv('DB_TIMEOUT', 10)),
    'pool_size': int(os.getenv('DB_POOL_SIZE', 5)),
    'pool_name': 'covid_analysis_pool'
}

# Application configuration
APP_CONFIG = {
    'title': 'COVID-19 Data Analysis',
    'theme': os.getenv('APP_THEME', 'litera'),
    'window_size': {
        'width': int(os.getenv('WINDOW_WIDTH', 1200)),
        'height': int(os.getenv('WINDOW_HEIGHT', 800))
    },
    'max_upload_size': int(os.getenv('MAX_UPLOAD_SIZE', 10 * 1024 * 1024)),  # 10MB
    'allowed_file_types': ['.csv']
}

# Privacy configuration
PRIVACY_CONFIG = {
    'epsilon': float(os.getenv('PRIVACY_EPSILON', 1.0)),
    'delta': float(os.getenv('PRIVACY_DELTA', 0.000001)),
    'sensitivity': float(os.getenv('PRIVACY_SENSITIVITY', 1.0)),
    'max_query_budget': float(os.getenv('MAX_QUERY_BUDGET', 10.0)),
    'noise_mechanism': os.getenv('NOISE_MECHANISM', 'gaussian'),  # or 'laplace'
    'minimum_query_size': int(os.getenv('MIN_QUERY_SIZE', 5))
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


# Ensure required directories exist
for directory in [os.path.join(BASE_DIR, 'logs')]:
    os.makedirs(directory, exist_ok=True)

# Initialize logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('Settings loaded successfully')

# Security settings (minimal exposure in settings file)
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
PASSWORD_SALT = os.getenv('PASSWORD_SALT', os.urandom(16).hex())
TOKEN_EXPIRY = int(os.getenv('TOKEN_EXPIRY', 24 * 60 * 60))  # 24 hours in seconds

# Development mode flag
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

if DEBUG:
    logger.warning('Application is running in DEBUG mode')