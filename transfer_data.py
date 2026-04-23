import psycopg2
import psycopg2.extras

LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "quant_trading",
    "user": "postgres",
    "password": "pass123"  # apna local password
}

RENDER_DB_URL = "postgresql://quant_trading_db_bn00_user:xmalVkiDxHizTFKjiAsYp8fPs6YlbmW7@dpg-d7htnrd7vvec739gcv40-a.singapore-postgres.render.com/quant_trading_db_bn00"  # apna Render URL yahan

def transfer():
    print("Connecting...")
    local = psycopg2.connect(**LOCAL_DB)
    render = psycopg2.connect(RENDER_DB_URL)

    lc = local.cursor()
    rc = render.cursor()

    # Prices transfer — batch mein
    print("Transferring prices...")
    lc.execute("SELECT stock, datetime, open, high, low, close, volume FROM prices")
    rows = lc.fetchall()
    psycopg2.extras.execute_values(rc, """
        INSERT INTO prices (stock, datetime, open, high, low, close, volume)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows, page_size=500)
    render.commit()
    print(f"Prices done: {len(rows)} rows!")

    # Sectors transfer — batch mein
    print("Transferring sectors...")
    lc.execute("SELECT sector_name, industry_name FROM sectors")
    rows = lc.fetchall()
    psycopg2.extras.execute_values(rc, """
        INSERT INTO sectors (sector_name, industry_name)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows, page_size=500)
    render.commit()
    print(f"Sectors done: {len(rows)} rows!")

    # Alt data transfer — batch mein
    print("Transferring alt_data...")
    lc.execute("SELECT stock, source, feature_name, value, datetime FROM alt_data")
    rows = lc.fetchall()
    psycopg2.extras.execute_values(rc, """
        INSERT INTO alt_data (stock, source, feature_name, value, datetime)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows, page_size=500)
    render.commit()
    print(f"Alt data done: {len(rows)} rows!")

    # Events transfer — batch mein
    print("Transferring events...")
    lc.execute("SELECT stock, event_type, datetime, raw_text FROM events")
    rows = lc.fetchall()
    psycopg2.extras.execute_values(rc, """
        INSERT INTO events (stock, event_type, datetime, raw_text)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows, page_size=500)
    render.commit()
    print(f"Events done: {len(rows)} rows!")

    local.close()
    render.close()
    print("\nAll data transferred successfully!")

if __name__ == "__main__":
    transfer()