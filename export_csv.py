import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
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

def export_to_csv():
    print("📤 Exporting data to CSV...\n")
    
    # Folder banao
    os.makedirs("sample_data", exist_ok=True)
    
    conn = get_connection()
    
    # Saara price data export karo
    df_prices = pd.read_sql("""
        SELECT * FROM prices 
        ORDER BY stock, datetime
    """, conn)
    
    df_prices.to_csv("sample_data/prices.csv", index=False)
    print(f"✅ prices.csv saved — {len(df_prices)} rows!")
    
    # Events data export karo
    df_events = pd.read_sql("""
        SELECT * FROM events 
        ORDER BY stock, datetime
    """, conn)
    
    df_events.to_csv("sample_data/events.csv", index=False)
    print(f"✅ events.csv saved — {len(df_events)} rows!")
    
    # Har stock ka alag CSV bhi banao
    stocks = df_prices['stock'].unique()
    for stock in stocks:
        stock_df = df_prices[df_prices['stock'] == stock]
        filename = f"sample_data/{stock.replace('.', '_')}.csv"
        stock_df.to_csv(filename, index=False)
    
    print(f"\n✅ Individual CSVs saved for {len(stocks)} stocks!")
    print("📁 Check 'sample_data' folder!")
    
    conn.close()

if __name__ == "__main__":
    export_to_csv()