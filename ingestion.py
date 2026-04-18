import yfinance as yf
import psycopg2
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# 20 Stocks ki list - Large cap, High liquidity, Different sectors
STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "LT.NS",
    "AXISBANK.NS", "WIPRO.NS", "HCLTECH.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "BAJFINANCE.NS", "ITC.NS"
]

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def fetch_and_store(symbol, start="2024-01-01", end="2025-01-01"):
    print(f"📥 Fetching data for {symbol}...")
    
    # Retry mechanism - 3 baar try karega
    for attempt in range(3):
        try:
            # yfinance se data fetch karo
            df = yf.download(symbol, start=start, end=end, auto_adjust=True)
            
            if df.empty:
                print(f"⚠️ No data found for {symbol}")
                return
            
            # Database mein save karo
            conn = get_connection()
            cursor = conn.cursor()
            
            inserted = 0
            for date, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO prices (stock, datetime, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (stock, datetime) DO NOTHING
                    """, (
                        symbol,
                        date,
                        float(row["Open"]),
                        float(row["High"]),
                        float(row["Low"]),
                        float(row["Close"]),
                        int(row["Volume"])
                    ))
                    inserted += 1
                except Exception as row_error:
                    print(f"⚠️ Row error for {symbol} on {date}: {row_error}")
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ {symbol} — {inserted} rows saved!")
            return  # success, bahar niklo
            
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed for {symbol}: {e}")
            time.sleep(2 ** attempt)  # exponential backoff: 1s, 2s, 4s
    
    print(f"❌ All 3 attempts failed for {symbol}")

def fetch_all_stocks():
    print("🚀 Starting data ingestion for all 20 stocks...\n")
    start_time = datetime.now()
    
    for symbol in STOCKS:
        fetch_and_store(symbol)
        time.sleep(1)  # API rate limit se bachne ke liye
    
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    print(f"\n🎉 All done! Total time: {duration} seconds")

if __name__ == "__main__":
    fetch_all_stocks()