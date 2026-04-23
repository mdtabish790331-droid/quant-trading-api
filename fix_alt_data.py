import psycopg2

RENDER_DB_URL = "postgresql://quant_trading_db_bn00_user:xmalVkiDxHizTFKjiAsYp8fPs6YlbmW7@dpg-d7htnrd7vvec739gcv40-a.singapore-postgres.render.com/quant_trading_db_bn00"

def fix_alt_data():
    print("Fixing alt_data duplicates...")
    conn = psycopg2.connect(RENDER_DB_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alt_data")
    print(f"Before: {cursor.fetchone()[0]} rows")

    cursor.execute("""
        DELETE FROM alt_data
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM alt_data
            GROUP BY stock, source, feature_name, datetime
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM alt_data")
    print(f"After: {cursor.fetchone()[0]} rows")
    cursor.close()
    conn.close()
    print("Alt data fixed! ✅")

if __name__ == "__main__":
    fix_alt_data()