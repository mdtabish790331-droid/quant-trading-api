import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),        # "localhost" nahi, "DB_HOST" 
        port=os.getenv("DB_PORT"),        # "5432" nahi, "DB_PORT"
        dbname=os.getenv("DB_NAME"),      # "quant_trading" nahi, "DB_NAME"
        user=os.getenv("DB_USER"),        # "postgres" nahi, "DB_USER"
        password=os.getenv("DB_PASSWORD") # "pass123" nahi, "DB_PASSWORD"
    )
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            stock VARCHAR(20) NOT NULL,
            datetime TIMESTAMP NOT NULL,
            open DOUBLE PRECISION NOT NULL,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume BIGINT NOT NULL,
            UNIQUE(stock, datetime)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            stock VARCHAR(20) NOT NULL,
            event_type VARCHAR(50) NOT NULL,
            datetime TIMESTAMP NOT NULL,
            raw_text TEXT NOT NULL
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables ready!")

if __name__ == "__main__":
    create_tables()