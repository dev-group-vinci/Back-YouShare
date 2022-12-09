import threading
from src.utils.logging import logger
import psycopg2
import os


class Db:

    __instance = None

    @staticmethod
    def getInstance():
        if Db.__instance is None:
            Db()
        return Db.__instance

    def __init__(self):
        if Db.__instance is not None:
            raise Exception("Db instance already exist !!")
        else:
            Db.__instance = self
            self.conn = None

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
