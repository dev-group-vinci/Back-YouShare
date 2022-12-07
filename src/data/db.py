import psycopg2
from dotenv import load_dotenv
import os


class Db:
    load_dotenv()

    def __init__(self):
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
            print("Database connection done")
        except(Exception, psycopg2.DatabaseError) as error:
            print("Database error")
            self.conn.close()
        return self.conn


