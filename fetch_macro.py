import yfinance as yf
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Macro Economic Indicators
MACRO_INDICATORS = {
    "^NSEI": "NIFTY50_Index",
    "^BSESN": "SENSEX_Index", 
    "GC=F": "Gold_Price",
    "CL=F": "Crude_Oil_Price",
    "EURINR=X": "EUR_INR_Rate",
    "USDINR=X": "USD_INR_Rate",
    "^TNX": "US_10Y_Treasury",
    "^VIX": "Volatility_Index",
}

def fetch_macro():
    print("📥 Fetching macro economic data...\n")

    conn = get_connection()
    cursor = conn.cursor()

    for symbol, feature_name in MACRO_INDICATORS.items():
        print(f"🔍 Fetching {feature_name}...")
        try:
            df = yf.download(
                symbol,
                start="2024-01-01",
                end="2025-01-01",
                auto_adjust=True
            )

            if df.empty:
                print(f"⚠️ No data for {feature_name}")
                continue

            inserted = 0
            for date, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO alt_data 
                        (stock, source, feature_name, value, datetime)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        symbol,
                        "macro_data",
                        feature_name,
                        float(row["Close"]),
                        date
                    ))
                    inserted += 1
                except Exception as row_err:
                    print(f"⚠️ Row error: {row_err}")

            conn.commit()
            print(f"✅ {feature_name} — {inserted} rows saved!")

        except Exception as e:
            print(f"❌ Error for {feature_name}: {e}")

    cursor.close()
    conn.close()
    print("\n🎉 All macro data fetched!")

if __name__ == "__main__":
    fetch_macro()