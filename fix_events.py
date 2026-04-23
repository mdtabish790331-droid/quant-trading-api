import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import random

RENDER_DB_URL = "postgresql://quant_trading_db_bn00_user:xmalVkiDxHizTFKjiAsYp8fPs6YlbmW7@dpg-d7htnrd7vvec739gcv40-a.singapore-postgres.render.com/quant_trading_db_bn00"

EVENTS = {
    "RELIANCE.NS": [
        ("EARNINGS", "Reliance Q3 FY24 net profit rises 11% to Rs 17,265 crore", "2024-01-15"),
        ("EARNINGS", "Reliance Q2 FY24 results: Revenue up 3% YoY", "2024-07-20"),
        ("DIVIDEND", "Reliance declares dividend of Rs 9 per share", "2024-08-30"),
        ("NEWS", "Reliance Jio adds 8.9 million subscribers in December", "2024-12-10"),
        ("NEWS", "Reliance Retail expands to 100 new cities", "2024-03-15"),
        ("BUYBACK", "Reliance announces Rs 10,000 crore buyback program", "2024-05-20"),
    ],
    "TCS.NS": [
        ("EARNINGS", "TCS Q3 FY24 net profit up 8.2% to Rs 11,058 crore", "2024-01-12"),
        ("EARNINGS", "TCS Q2 FY24 revenue grows 7.8% YoY", "2024-07-11"),
        ("DIVIDEND", "TCS declares interim dividend of Rs 27 per share", "2024-10-10"),
        ("NEWS", "TCS wins $2.2 billion deal with UK pension company", "2024-04-05"),
        ("NEWS", "TCS to hire 40,000 freshers in FY25", "2024-02-20"),
    ],
    "HDFCBANK.NS": [
        ("EARNINGS", "HDFC Bank Q3 FY24 net profit rises 34% to Rs 16,373 crore", "2024-01-16"),
        ("EARNINGS", "HDFC Bank Q2 FY24 NII grows 30% post merger", "2024-07-20"),
        ("DIVIDEND", "HDFC Bank declares dividend of Rs 19.50 per share", "2024-05-15"),
        ("NEWS", "HDFC Bank completes merger with HDFC Ltd successfully", "2024-03-10"),
    ],
    "INFY.NS": [
        ("EARNINGS", "Infosys Q3 FY24 net profit rises 7.3% to Rs 6,106 crore", "2024-01-11"),
        ("EARNINGS", "Infosys Q2 FY24 revenue at Rs 38,994 crore", "2024-07-18"),
        ("DIVIDEND", "Infosys declares interim dividend of Rs 18 per share", "2024-10-17"),
        ("NEWS", "Infosys launches generative AI platform Topaz", "2024-06-12"),
    ],
    "ICICIBANK.NS": [
        ("EARNINGS", "ICICI Bank Q3 FY24 profit jumps 23% to Rs 10,272 crore", "2024-01-20"),
        ("DIVIDEND", "ICICI Bank declares dividend of Rs 8 per share", "2024-08-10"),
        ("NEWS", "ICICI Bank launches AI-based fraud detection system", "2024-05-22"),
    ],
    "SBIN.NS": [
        ("EARNINGS", "SBI Q3 FY24 net profit rises 35% to Rs 9,164 crore", "2024-02-03"),
        ("DIVIDEND", "SBI declares dividend of Rs 11.30 per share", "2024-06-15"),
        ("NEWS", "SBI targets Rs 100 lakh crore loan book by FY25", "2024-04-18"),
    ],
    "WIPRO.NS": [
        ("EARNINGS", "Wipro Q3 FY24 net profit at Rs 2,694 crore", "2024-01-10"),
        ("DIVIDEND", "Wipro declares interim dividend of Rs 1 per share", "2024-10-20"),
        ("NEWS", "Wipro launches AI360 strategy for enterprise clients", "2024-07-05"),
    ],
    "BHARTIARTL.NS": [
        ("EARNINGS", "Airtel Q3 FY24 profit jumps 54% to Rs 2,442 crore", "2024-02-01"),
        ("NEWS", "Airtel adds 3.2 million 5G users in December", "2024-12-15"),
        ("NEWS", "Airtel completes 5G rollout in 500 cities", "2024-09-20"),
    ],
    "KOTAKBANK.NS": [
        ("EARNINGS", "Kotak Bank Q3 FY24 net profit up 9% to Rs 3,005 crore", "2024-01-20"),
        ("DIVIDEND", "Kotak Bank declares dividend of Rs 2 per share", "2024-07-15"),
        ("NEWS", "Kotak Bank launches UPI-based credit on credit card", "2024-05-10"),
    ],
    "LT.NS": [
        ("EARNINGS", "L&T Q3 FY24 net profit rises 15% to Rs 2,947 crore", "2024-01-25"),
        ("EARNINGS", "L&T Q2 FY24 order inflow at Rs 77,000 crore", "2024-07-22"),
        ("NEWS", "L&T wins Rs 7,000 crore infrastructure project", "2024-03-18"),
    ],
    "AXISBANK.NS": [
        ("EARNINGS", "Axis Bank Q3 FY24 profit up 4% to Rs 6,071 crore", "2024-01-23"),
        ("DIVIDEND", "Axis Bank declares dividend of Rs 1 per share", "2024-06-20"),
        ("NEWS", "Axis Bank completes Citibank India acquisition integration", "2024-04-12"),
    ],
    "HCLTECH.NS": [
        ("EARNINGS", "HCL Tech Q3 FY24 profit up 6.2% to Rs 4,350 crore", "2024-01-13"),
        ("DIVIDEND", "HCL Tech declares special dividend of Rs 18 per share", "2024-10-22"),
        ("NEWS", "HCL Tech wins 5-year deal with German automotive company", "2024-06-08"),
    ],
    "ASIANPAINT.NS": [
        ("EARNINGS", "Asian Paints Q3 FY24 profit falls 25% on higher costs", "2024-01-19"),
        ("DIVIDEND", "Asian Paints declares dividend of Rs 21.35 per share", "2024-05-28"),
        ("NEWS", "Asian Paints enters waterproofing market with new range", "2024-08-15"),
    ],
    "MARUTI.NS": [
        ("EARNINGS", "Maruti Q3 FY24 profit jumps 33% to Rs 3,130 crore", "2024-01-26"),
        ("EARNINGS", "Maruti Q2 FY24 sales volume hits record 5.5 lakh units", "2024-07-25"),
        ("NEWS", "Maruti Suzuki launches new Swift with hybrid technology", "2024-05-05"),
    ],
    "TITAN.NS": [
        ("EARNINGS", "Titan Q3 FY24 revenue up 20% to Rs 12,202 crore", "2024-02-08"),
        ("DIVIDEND", "Titan declares dividend of Rs 11 per share", "2024-08-20"),
        ("NEWS", "Titan Jewellery division grows 25% in festive quarter", "2024-10-28"),
    ],
    "SUNPHARMA.NS": [
        ("EARNINGS", "Sun Pharma Q3 FY24 profit up 28% to Rs 2,809 crore", "2024-02-06"),
        ("DIVIDEND", "Sun Pharma declares dividend of Rs 3.25 per share", "2024-08-22"),
        ("NEWS", "Sun Pharma US specialty revenue crosses $500 million", "2024-11-10"),
    ],
    "ULTRACEMCO.NS": [
        ("EARNINGS", "UltraTech Cement Q3 FY24 profit up 69% to Rs 1,777 crore", "2024-01-30"),
        ("NEWS", "UltraTech acquires India Cements for Rs 3,954 crore", "2024-09-05"),
        ("DIVIDEND", "UltraTech declares dividend of Rs 38 per share", "2024-05-18"),
    ],
    "BAJFINANCE.NS": [
        ("EARNINGS", "Bajaj Finance Q3 FY24 profit up 22% to Rs 3,639 crore", "2024-01-24"),
        ("DIVIDEND", "Bajaj Finance declares dividend of Rs 36 per share", "2024-07-30"),
        ("NEWS", "Bajaj Finance AUM crosses Rs 3.25 lakh crore milestone", "2024-11-20"),
    ],
    "HINDUNILVR.NS": [
        ("EARNINGS", "HUL Q3 FY24 profit up 0.6% to Rs 2,519 crore", "2024-01-22"),
        ("DIVIDEND", "HUL declares interim dividend of Rs 19 per share", "2024-10-25"),
        ("NEWS", "HUL launches premium skincare range in India", "2024-06-18"),
    ],
    "ITC.NS": [
        ("EARNINGS", "ITC Q3 FY24 profit up 8.4% to Rs 5,640 crore", "2024-01-28"),
        ("DIVIDEND", "ITC declares dividend of Rs 7.50 per share", "2024-07-08"),
        ("NEWS", "ITC Hotels demerger approved by board of directors", "2024-03-25"),
        ("NEWS", "ITC FMCG business revenue crosses Rs 20,000 crore", "2024-09-15"),
    ],
}

def fix_events():
    print("Connecting to Render DB...")
    conn = psycopg2.connect(RENDER_DB_URL)
    cursor = conn.cursor()

    # Saare events delete karo
    cursor.execute("DELETE FROM events")
    conn.commit()
    print("Old events deleted!")

    # Fresh events insert karo
    total = 0
    for stock, events in EVENTS.items():
        for event_type, raw_text, date_str in events:
            cursor.execute("""
                INSERT INTO events (stock, event_type, datetime, raw_text)
                VALUES (%s, %s, %s, %s)
            """, (stock, event_type, date_str, raw_text))
            total += 1

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM events")
    print(f"Total events inserted: {cursor.fetchone()[0]}")
    cursor.close()
    conn.close()
    print("Events fixed! ✅")

if __name__ == "__main__":
    fix_events()