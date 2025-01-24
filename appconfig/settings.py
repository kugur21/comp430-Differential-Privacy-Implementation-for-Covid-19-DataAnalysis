import os
from dotenv import load_dotenv
import logging.config


# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', 3306)),
    'raise_on_warnings': True,
    'connection_timeout': int(os.getenv('DB_TIMEOUT', 10)),
    'pool_size': int(os.getenv('DB_POOL_SIZE', 5)),
    'pool_name': 'covid_analysis_pool'
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

# Initialize logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('Settings loaded successfully')