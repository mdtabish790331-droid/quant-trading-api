import psycopg2
import os

# Yahan Render ka External Database URL paste karo
RENDER_DB_URL = "postgresql://quant_trading_db_bn00_user:xmalVkiDxHizTFKjiAsYp8fPs6YlbmW7@dpg-d7htnrd7vvec739gcv40-a.singapore-postgres.render.com/quant_trading_db_bn00"

def setup():
    print("Connecting to Render DB...")
    conn = psycopg2.connect(RENDER_DB_URL)
    cursor = conn.cursor()

    # Tables banao
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sectors (
            id SERIAL PRIMARY KEY,
            sector_name TEXT NOT NULL,
            industry_name TEXT NOT NULL,
            num_companies INT DEFAULT 0,
            median_pe FLOAT DEFAULT 0,
            sales_growth FLOAT DEFAULT 0,
            opm FLOAT DEFAULT 0,
            roce FLOAT DEFAULT 0,
            median_return FLOAT DEFAULT 0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alt_data (
            id SERIAL PRIMARY KEY,
            stock TEXT NOT NULL,
            source TEXT NOT NULL,
            feature_name TEXT NOT NULL,
            value FLOAT,
            datetime TIMESTAMP NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables ready!")

if __name__ == "__main__":
    setup()