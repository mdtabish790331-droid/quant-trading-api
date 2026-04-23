import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    return conn

def load_data(stock):
    conn = get_connection()

    query = f"""
    SELECT datetime, open, high, low, close, volume
    FROM prices
    WHERE stock = '{stock}'
    ORDER BY datetime
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df