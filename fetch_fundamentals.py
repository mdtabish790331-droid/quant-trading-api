import yfinance as yf
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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

def fetch_fundamentals():
    print("📥 Fetching fundamental data...\n")

    conn = get_connection()
    cursor = conn.cursor()

    # Alt data table mein store karenge
    for symbol in STOCKS:
        print(f"🔍 Fetching fundamentals for {symbol}...")
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Jo data milta hai usse store karo
            features = {
                "pe_ratio": info.get("trailingPE", None),
                "eps": info.get("trailingEps", None),
                "revenue": info.get("totalRevenue", None),
                "ebitda": info.get("ebitda", None),
                "profit_margin": info.get("profitMargins", None),
                "debt_to_equity": info.get("debtToEquity", None),
                "return_on_equity": info.get("returnOnEquity", None),
                "market_cap": info.get("marketCap", None),
            }

            for feature_name, value in features.items():
                if value is not None:
                    cursor.execute("""
                        INSERT INTO alt_data 
                        (stock, source, feature_name, value, datetime)
                        VALUES (%s, %s, %s, %s, NOW())
                        ON CONFLICT DO NOTHING
                    """, (symbol, "yfinance_fundamentals", feature_name, float(value)))

            print(f"✅ {symbol} fundamentals saved!")

        except Exception as e:
            print(f"❌ Error for {symbol}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 All fundamentals fetched!")

if __name__ == "__main__":
    fetch_fundamentals()