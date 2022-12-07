import threading
from src.utils.logging import logger
import psycopg2
from dotenv import load_dotenv
import os


class Db:
    load_dotenv()

    def __init__(self):
        self.conn = None
        self.connection = threading.local()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                port=os.getenv("DB_PORT"),
            )

            self.conn.autocommit = False

            logger.info("Database connection done")
        except(Exception, psycopg2.DatabaseError) as error:
            logger.warning(error)
            self.conn.close()
        return self.conn

    def close(self):
        try:
            self.conn.close()
        except(Exception, psycopg2.InternalError) as error:
            self.conn = None
            logger.warning(error)
