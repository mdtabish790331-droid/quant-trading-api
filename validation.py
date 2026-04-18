import psycopg2
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

def validate_all_data():
    print("🔍 Validating all data...\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    errors = []
    
    # Rule 1: High >= max(Open, Close)
    cursor.execute("""
        SELECT stock, datetime, open, high, close 
        FROM prices 
        WHERE high < open OR high < close
    """)
    bad_high = cursor.fetchall()
    if bad_high:
        for row in bad_high:
            errors.append(f"❌ HIGH error: {row[0]} on {row[1]} — High={row[3]}, Open={row[2]}, Close={row[4]}")
    
    # Rule 2: Low <= min(Open, Close)
    cursor.execute("""
        SELECT stock, datetime, open, low, close 
        FROM prices 
        WHERE low > open OR low > close
    """)
    bad_low = cursor.fetchall()
    if bad_low:
        for row in bad_low:
            errors.append(f"❌ LOW error: {row[0]} on {row[1]} — Low={row[3]}, Open={row[2]}, Close={row[4]}")
    
    # Rule 3: Volume >= 0
    cursor.execute("""
        SELECT stock, datetime, volume 
        FROM prices 
        WHERE volume < 0
    """)
    bad_volume = cursor.fetchall()
    if bad_volume:
        for row in bad_volume:
            errors.append(f"❌ VOLUME error: {row[0]} on {row[1]} — Volume={row[2]}")
    
    # Rule 4: Null values check
    cursor.execute("""
        SELECT COUNT(*) FROM prices 
        WHERE stock IS NULL OR datetime IS NULL OR 
              open IS NULL OR high IS NULL OR 
              low IS NULL OR close IS NULL OR volume IS NULL
    """)
    null_count = cursor.fetchone()[0]
    if null_count > 0:
        errors.append(f"❌ NULL values found: {null_count} rows")
    
    cursor.close()
    conn.close()
    
    # Result
    if errors:
        print("⚠️ Validation Issues Found:")
        for e in errors:
            print(e)
    else:
        print("✅ All data is valid! No issues found.")
    
    # Summary
    print(f"\n📊 Total issues found: {len(errors)}")
    return len(errors) == 0

if __name__ == "__main__":
    validate_all_data()