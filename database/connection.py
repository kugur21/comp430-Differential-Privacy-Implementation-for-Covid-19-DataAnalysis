import mysql.connector
from mysql.connector import Error, pooling
from config.settings import DB_CONFIG
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.pool = None
        self._setup_connection_pool()

    def _setup_connection_pool(self):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=DB_CONFIG['pool_name'],
                pool_size=DB_CONFIG['pool_size'],
                **{k: v for k, v in DB_CONFIG.items() if k not in ['pool_name', 'pool_size']}
            )
            logger.info("Connection pool created successfully")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = self.pool.get_connection()
                self.cursor = self.connection.cursor(buffered=True, dictionary=True)
                logger.info("Successfully connected to the database")
            return True
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return False

    def execute_query(self, query, params=None):
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            return False

    def execute_many(self, query, params_list):
        try:
            self.connect()
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Error executing batch query: {e}")
            self.connection.rollback()
            return False

    def fetchone(self):
        return self.cursor.fetchone() if self.cursor else None

    def fetchall(self):
        return self.cursor.fetchall() if self.cursor else []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")