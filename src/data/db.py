import threading
from src.utils.logging import logger
import psycopg2.pool
import psycopg2
import os


class Db:
    _local = threading.local()

    @staticmethod
    def getInstance():
        if not hasattr(Db._local, "instance"):
            Db._local.instance = Db()
        return Db._local.instance

    def __init__(self):
        self.conn = None
        self.pool = None

    def connect(self):
        try:
            if self.pool is None:
                self.pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=5,
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS"),
                    port=os.getenv("DB_PORT"),
                )

                logger.info("Database connection done")
        except(Exception, psycopg2.DatabaseError) as error:
            logger.warning(error)
            raise error

    def getConnection(self):
        if self.conn is None:
            self.conn = self.pool.getconn()
            self.conn.autocommit = False
        return self.conn

    def freeConnexion(self):
        try:
            if self.pool and self.conn:
                self.pool.putconn(self.conn)
                self.conn = None
        except(Exception, psycopg2.InternalError) as error:
            self.conn = None
            logger.warning(error)
