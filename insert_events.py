import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

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

STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "LT.NS",
    "AXISBANK.NS", "WIPRO.NS", "HCLTECH.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "BAJFINANCE.NS", "ITC.NS"
]

EVENTS = {
    "RELIANCE.NS": [
        ("EARNINGS", "Reliance Q3 FY24 net profit rises 11% to Rs 17,265 crore"),
        ("EARNINGS", "Reliance Q2 FY24 results: Revenue up 3% YoY"),
        ("DIVIDEND", "Reliance declares dividend of Rs 9 per share"),
        ("NEWS", "Reliance Jio adds 8.9 million subscribers in December"),
        ("NEWS", "Reliance Retail expands to 100 new cities"),
        ("BUYBACK", "Reliance announces Rs 10,000 crore buyback program"),
        ("NEWS", "Reliance Industries targets net zero carbon by 2035"),
    ],
    "TCS.NS": [
        ("EARNINGS", "TCS Q3 FY24 net profit up 8.2% to Rs 11,058 crore"),
        ("EARNINGS", "TCS Q2 FY24 revenue grows 7.8% YoY in constant currency"),
        ("DIVIDEND", "TCS declares interim dividend of Rs 27 per share"),
        ("NEWS", "TCS wins $2.2 billion deal with UK pension company"),
        ("NEWS", "TCS to hire 40,000 freshers in FY25"),
        ("NEWS", "TCS launches AI-powered cloud migration platform"),
    ],
    "HDFCBANK.NS": [
        ("EARNINGS", "HDFC Bank Q3 FY24 net profit rises 34% to Rs 16,373 crore"),
        ("EARNINGS", "HDFC Bank Q2 FY24 NII grows 30% post merger"),
        ("DIVIDEND", "HDFC Bank declares dividend of Rs 19.50 per share"),
        ("NEWS", "HDFC Bank completes merger with HDFC Ltd successfully"),
        ("NEWS", "HDFC Bank targets 1.5x balance sheet growth in 3 years"),
    ],
    "INFY.NS": [
        ("EARNINGS", "Infosys Q3 FY24 net profit rises 7.3% to Rs 6,106 crore"),
        ("EARNINGS", "Infosys Q2 FY24 revenue at Rs 38,994 crore"),
        ("DIVIDEND", "Infosys declares interim dividend of Rs 18 per share"),
        ("NEWS", "Infosys wins multi-million dollar deal with European bank"),
        ("NEWS", "Infosys launches generative AI platform Topaz"),
    ],
    "ICICIBANK.NS": [
        ("EARNINGS", "ICICI Bank Q3 FY24 profit jumps 23% to Rs 10,272 crore"),
        ("EARNINGS", "ICICI Bank Q2 FY24 NII up 24% YoY"),
        ("DIVIDEND", "ICICI Bank declares dividend of Rs 8 per share"),
        ("NEWS", "ICICI Bank launches AI-based fraud detection system"),
    ],
    "SBIN.NS": [
        ("EARNINGS", "SBI Q3 FY24 net profit rises 35% to Rs 9,164 crore"),
        ("EARNINGS", "SBI Q2 FY24 NIM improves to 3.43%"),
        ("DIVIDEND", "SBI declares dividend of Rs 11.30 per share"),
        ("NEWS", "SBI targets Rs 100 lakh crore loan book by FY25"),
    ],
    "WIPRO.NS": [
        ("EARNINGS", "Wipro Q3 FY24 net profit at Rs 2,694 crore"),
        ("EARNINGS", "Wipro Q2 FY24 IT revenue at $2.77 billion"),
        ("DIVIDEND", "Wipro declares interim dividend of Rs 1 per share"),
        ("NEWS", "Wipro launches AI360 strategy for enterprise clients"),
    ],
    "BHARTIARTL.NS": [
        ("EARNINGS", "Airtel Q3 FY24 profit jumps 54% to Rs 2,442 crore"),
        ("EARNINGS", "Airtel Q2 FY24 ARPU rises to Rs 203"),
        ("NEWS", "Airtel adds 3.2 million 5G users in December"),
        ("NEWS", "Airtel completes 5G rollout in 500 cities"),
    ],
    "KOTAKBANK.NS": [
        ("EARNINGS", "Kotak Bank Q3 FY24 net profit up 9% to Rs 3,005 crore"),
        ("DIVIDEND", "Kotak Bank declares dividend of Rs 2 per share"),
        ("NEWS", "Kotak Bank launches UPI-based credit on credit card"),
    ],
    "LT.NS": [
        ("EARNINGS", "L&T Q3 FY24 net profit rises 15% to Rs 2,947 crore"),
        ("EARNINGS", "L&T Q2 FY24 order inflow at Rs 77,000 crore"),
        ("NEWS", "L&T wins Rs 7,000 crore infrastructure project"),
        ("NEWS", "L&T Technology wins EV platform deal from US automaker"),
    ],
    "AXISBANK.NS": [
        ("EARNINGS", "Axis Bank Q3 FY24 profit up 4% to Rs 6,071 crore"),
        ("DIVIDEND", "Axis Bank declares dividend of Rs 1 per share"),
        ("NEWS", "Axis Bank completes Citibank India acquisition integration"),
    ],
    "HCLTECH.NS": [
        ("EARNINGS", "HCL Tech Q3 FY24 profit up 6.2% to Rs 4,350 crore"),
        ("DIVIDEND", "HCL Tech declares special dividend of Rs 18 per share"),
        ("NEWS", "HCL Tech wins 5-year deal with German automotive company"),
    ],
    "ASIANPAINT.NS": [
        ("EARNINGS", "Asian Paints Q3 FY24 profit falls 25% on higher costs"),
        ("DIVIDEND", "Asian Paints declares dividend of Rs 21.35 per share"),
        ("NEWS", "Asian Paints enters waterproofing market with new range"),
    ],
    "MARUTI.NS": [
        ("EARNINGS", "Maruti Q3 FY24 profit jumps 33% to Rs 3,130 crore"),
        ("EARNINGS", "Maruti Q2 FY24 sales volume hits record 5.5 lakh units"),
        ("NEWS", "Maruti Suzuki launches new Swift with hybrid technology"),
        ("NEWS", "Maruti targets 4 lakh EV sales by 2030"),
    ],
    "TITAN.NS": [
        ("EARNINGS", "Titan Q3 FY24 revenue up 20% to Rs 12,202 crore"),
        ("DIVIDEND", "Titan declares dividend of Rs 11 per share"),
        ("NEWS", "Titan Jewellery division grows 25% in festive quarter"),
    ],
    "SUNPHARMA.NS": [
        ("EARNINGS", "Sun Pharma Q3 FY24 profit up 28% to Rs 2,809 crore"),
        ("DIVIDEND", "Sun Pharma declares dividend of Rs 3.25 per share"),
        ("NEWS", "Sun Pharma US specialty revenue crosses $500 million"),
    ],
    "ULTRACEMCO.NS": [
        ("EARNINGS", "UltraTech Cement Q3 FY24 profit up 69% to Rs 1,777 crore"),
        ("NEWS", "UltraTech acquires India Cements for Rs 3,954 crore"),
        ("DIVIDEND", "UltraTech declares dividend of Rs 38 per share"),
    ],
    "BAJFINANCE.NS": [
        ("EARNINGS", "Bajaj Finance Q3 FY24 profit up 22% to Rs 3,639 crore"),
        ("DIVIDEND", "Bajaj Finance declares dividend of Rs 36 per share"),
        ("NEWS", "Bajaj Finance AUM crosses Rs 3.25 lakh crore milestone"),
    ],
    "HINDUNILVR.NS": [
        ("EARNINGS", "HUL Q3 FY24 profit up 0.6% to Rs 2,519 crore"),
        ("DIVIDEND", "HUL declares interim dividend of Rs 19 per share"),
        ("NEWS", "HUL launches premium skincare range in India"),
    ],
    "ITC.NS": [
        ("EARNINGS", "ITC Q3 FY24 profit up 8.4% to Rs 5,640 crore"),
        ("DIVIDEND", "ITC declares dividend of Rs 7.50 per share"),
        ("NEWS", "ITC Hotels demerger approved by board of directors"),
        ("NEWS", "ITC FMCG business revenue crosses Rs 20,000 crore"),
    ],
}

def insert_events():
    print("📰 Inserting events data...\n")
    conn = get_connection()
    cursor = conn.cursor()

    total = 0
    base_date = datetime(2024, 1, 1)

    for stock, events in EVENTS.items():
        print(f"📥 Inserting events for {stock}...")
        for i, (event_type, raw_text) in enumerate(events):
            event_date = base_date + timedelta(days=random.randint(1, 365))
            cursor.execute("""
                INSERT INTO events (stock, event_type, datetime, raw_text)
                VALUES (%s, %s, %s, %s)
            """, (stock, event_type, event_date, raw_text))
            total += 1

        conn.commit()
        print(f"✅ {stock} — {len(events)} events inserted!")

    cursor.close()
    conn.close()
    print(f"\n🎉 Total {total} events inserted successfully!")

if __name__ == "__main__":
    insert_events()