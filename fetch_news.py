import yfinance as yf
import psycopg2
import os
import hashlib
from dotenv import load_dotenv
from datetime import datetime

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

def clean_title(title):
    """
    Title ko clean karo duplicate detect karne ke liye
    - Lowercase karo
    - Extra spaces hatao
    - Special characters hatao
    """
    import re
    title = title.lower().strip()
    title = re.sub(r'[^a-z0-9\s]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title

def get_title_hash(title):
    """
    Title ka unique hash banao
    Same title = Same hash → Duplicate detect hoga
    """
    cleaned = clean_title(title)
    return hashlib.md5(cleaned.encode()).hexdigest()

def get_existing_hashes(cursor, stock):
    """
    Database mein already stored news ke hashes lo
    """
    cursor.execute("""
        SELECT raw_text FROM events
        WHERE stock = %s AND event_type = 'NEWS'
    """, (stock,))
    rows = cursor.fetchall()

    existing_hashes = set()
    for row in rows:
        # raw_text mein hash stored hai
        if row[0] and row[0].startswith("HASH:"):
            existing_hashes.add(row[0].split("HASH:")[1].split("|")[0])
    return existing_hashes

def is_similar_title(title1, title2, threshold=0.7):
    """
    Do titles kitni similar hain check karo
    Example:
    "Tata Motors Q3 Results" vs "Tata Motors Q3 Earnings"
    → 80% similar → Duplicate!
    """
    words1 = set(clean_title(title1).split())
    words2 = set(clean_title(title2).split())

    if not words1 or not words2:
        return False

    # Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    similarity = len(intersection) / len(union)

    return similarity >= threshold

def fetch_news():
    print("📰 Fetching news with duplicate detection...\n")

    conn = get_connection()
    cursor = conn.cursor()

    total_inserted = 0
    total_duplicates = 0
    total_similar = 0

    for symbol in STOCKS:
        print(f"🔍 Fetching news for {symbol}...")
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news

            if not news:
                print(f"⚠️  No news for {symbol}\n")
                continue

            # Already stored hashes lo
            existing_hashes = get_existing_hashes(cursor, symbol)

            # Is session mein jo titles aaye unka track
            session_titles = []

            inserted = 0
            duplicates = 0
            similar = 0

            for article in news:
                try:
                    title = article.get("title", "").strip()
                    if not title:
                        continue

                    # Step 1: Exact duplicate check (Hash se)
                    title_hash = get_title_hash(title)
                    if title_hash in existing_hashes:
                        duplicates += 1
                        continue

                    # Step 2: Similar title check
                    is_dup = False
                    for prev_title in session_titles:
                        if is_similar_title(title, prev_title):
                            similar += 1
                            is_dup = True
                            break

                    if is_dup:
                        continue

                    # Step 3: Timestamp
                    pub_time = article.get("providerPublishTime", None)
                    if pub_time:
                        news_date = datetime.fromtimestamp(pub_time)
                    else:
                        news_date = datetime.now()

                    # Step 4: Save karo
                    # raw_text mein hash + title store karo
                    raw_text = f"HASH:{title_hash}|TITLE:{title}"

                    cursor.execute("""
                        INSERT INTO events
                        (stock, event_type, datetime, raw_text)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        symbol,
                        "NEWS",
                        news_date,
                        raw_text
                    ))

                    # Alt data mein news count
                    cursor.execute("""
                        INSERT INTO alt_data
                        (stock, source, feature_name, value, datetime)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        symbol,
                        "news_sentiment",
                        "news_count",
                        1.0,
                        news_date
                    ))

                    # Track karo
                    existing_hashes.add(title_hash)
                    session_titles.append(title)
                    inserted += 1

                except Exception as row_err:
                    print(f"⚠️  Row error: {row_err}")

            conn.commit()

            total_inserted += inserted
            total_duplicates += duplicates
            total_similar += similar

            print(f"✅ {symbol}:")
            print(f"   📥 Inserted  : {inserted}")
            print(f"   🔁 Exact Dup : {duplicates}")
            print(f"   🔀 Similar   : {similar}")
            print()

        except Exception as e:
            print(f"❌ Error for {symbol}: {e}\n")

    cursor.close()
    conn.close()

    print("=" * 40)
    print(f"🎉 News fetch complete!")
    print(f"   ✅ Total Inserted  : {total_inserted}")
    print(f"   🔁 Exact Dupes    : {total_duplicates}")
    print(f"   🔀 Similar Dupes  : {total_similar}")
    print("=" * 40)

if __name__ == "__main__":
    fetch_news()