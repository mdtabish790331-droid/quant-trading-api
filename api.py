from fastapi import FastAPI, HTTPException
import psycopg2
from datetime import date
import os
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Quant Trading API", version="1.0.0")

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Render par hai — DATABASE_URL use karo
        conn = psycopg2.connect(database_url)
    else:
        # Local machine par hai — .env use karo
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    return conn

@app.get("/")
def home():
    return {"message": "✅ Quant Trading API is running!"}

@app.get("/stocks")
def get_all_stocks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT stock, COUNT(*) as total_rows
            FROM prices
            GROUP BY stock
            ORDER BY stock
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        stocks = [{"stock": r[0], "total_rows": r[1]} for r in rows]
        return {"total_stocks": len(stocks), "stocks": stocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prices/{stock}")
def get_prices(stock: str, start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT stock, datetime, open, high, low, close, volume
            FROM prices
            WHERE stock = %s 
            AND datetime BETWEEN %s AND %s
            ORDER BY datetime ASC
        """, (stock.upper(), start_date, end_date))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail=f"No data found for {stock}")
        data = [
            {
                "stock": r[0],
                "datetime": str(r[1]),
                "open": r[2],
                "high": r[3],
                "low": r[4],
                "close": r[5],
                "volume": r[6]
            }
            for r in rows
        ]
        return {"stock": stock.upper(), "total_rows": len(data), "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{stock}")
def get_events(stock: str, start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT stock, event_type, datetime, raw_text
            FROM events
            WHERE stock = %s 
            AND datetime BETWEEN %s AND %s
            ORDER BY datetime ASC
        """, (stock.upper(), start_date, end_date))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        data = [
            {
                "stock": r[0],
                "event_type": r[1],
                "datetime": str(r[2]),
                "raw_text": r[3]
            }
            for r in rows
        ]
        return {"stock": stock.upper(), "total_events": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backtest/{stock}")
def run_backtest(stock: str):
    try:
        from data_loader import load_data
        from utils.strategy.moving_average import generate_signals
        from utils.strategy.backtest.engine import backtest

        df = load_data(stock.upper())

        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")

        df = generate_signals(df)
        final_value, trades = backtest(df)

        return {
            "stock": stock.upper(),
            "initial_capital": 100000,
            "final_value": round(final_value, 2),
            "profit": round(final_value - 100000, 2),
            "total_trades": len(trades),
            "trades": trades
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sectors")
def get_all_sectors():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sector_name, industry_name
            FROM sectors
            ORDER BY sector_name
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "total_sectors": len(rows),
            "sectors": [
                {"sector_name": r[0], "industry_name": r[1]}
                for r in rows
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sector/{sector_name}")
def get_sector_data(sector_name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sector_name, industry_name, num_companies,
                   median_pe, sales_growth, opm, roce, median_return
            FROM sectors
            WHERE LOWER(sector_name) LIKE LOWER(%s)
            ORDER BY sector_name
        """, (f"%{sector_name}%",))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail=f"Sector not found: {sector_name}")
        data = [
            {
                "sector_name": r[0],
                "industry_name": r[1],
                "num_companies": r[2],
                "median_pe": r[3],
                "sales_growth": r[4],
                "opm": r[5],
                "roce": r[6],
                "median_return": r[7]
            }
            for r in rows
        ]
        return {"sector": sector_name, "total_results": len(data), "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alt_data/{stock}")
def get_alt_data(stock: str, feature: str = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if feature:
            cursor.execute("""
                SELECT stock, source, feature_name, value, datetime
                FROM alt_data
                WHERE stock = %s AND feature_name = %s
                ORDER BY datetime DESC
            """, (stock.upper(), feature))
        else:
            cursor.execute("""
                SELECT stock, source, feature_name, value, datetime
                FROM alt_data
                WHERE stock = %s
                ORDER BY datetime DESC
            """, (stock.upper(),))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail=f"No alt data found for {stock}")
        data = [
            {
                "stock": r[0],
                "source": r[1],
                "feature_name": r[2],
                "value": r[3],
                "datetime": str(r[4])
            }
            for r in rows
        ]
        return {"stock": stock.upper(), "total_results": len(data), "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/features/{stock}")
def get_all_features(stock: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT feature_name, source
            FROM alt_data
            WHERE stock = %s
        """, (stock.upper(),))
        features = cursor.fetchall()
        cursor.execute("""
            SELECT feature_name, value, datetime, source
            FROM alt_data
            WHERE stock = %s
            ORDER BY datetime DESC
        """, (stock.upper(),))
        latest = cursor.fetchall()
        cursor.close()
        conn.close()
        return {
            "stock": stock.upper(),
            "total_features": len(features),
            "features": [{"name": f[0], "source": f[1]} for f in features],
            "latest_values": [
                {
                    "feature": r[0],
                    "value": r[1],
                    "datetime": str(r[2]),
                    "source": r[3]
                }
                for r in latest[:20]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Quant Trading API</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { color: #333; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { padding: 8px; width: 100%; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>📈 Quant Trading API</h1>

    <div class="form-group">
        <label>Stock:</label>
        <select id="stock">
            <option>RELIANCE.NS</option>
            <option>TCS.NS</option>
            <option>HDFCBANK.NS</option>
            <option>INFY.NS</option>
            <option>HINDUNILVR.NS</option>
            <option>ICICIBANK.NS</option>
            <option>SBIN.NS</option>
            <option>BHARTIARTL.NS</option>
            <option>KOTAKBANK.NS</option>
            <option>LT.NS</option>
            <option>AXISBANK.NS</option>
            <option>WIPRO.NS</option>
            <option>HCLTECH.NS</option>
            <option>ASIANPAINT.NS</option>
            <option>MARUTI.NS</option>
            <option>TITAN.NS</option>
            <option>SUNPHARMA.NS</option>
            <option>ULTRACEMCO.NS</option>
            <option>BAJFINANCE.NS</option>
            <option>ITC.NS</option>
        </select>
    </div>

    <div class="form-group">
        <label>Start Date:</label>
        <input type="date" id="start_date" value="2024-01-01">
    </div>

    <div class="form-group">
        <label>End Date:</label>
        <input type="date" id="end_date" value="2024-12-31">
    </div>

    <div class="form-group">
        <label>Data Type:</label>
        <select id="data_type">
            <option value="prices">Price Data</option>
            <option value="events">Events & News</option>
            <option value="alt_data">Alternative Data</option>
        </select>
    </div>

    <button onclick="fetchData()">Fetch Data</button>

    <h3 id="result_title"></h3>
    <pre id="result">Data will appear here...</pre>

    <script>
        async function fetchData() {
            const stock = document.getElementById('stock').value;
            const start = document.getElementById('start_date').value;
            const end = document.getElementById('end_date').value;
            const type = document.getElementById('data_type').value;

            let url = '';
            if (type === 'prices') {
                url = `/prices/${stock}?start_date=${start}&end_date=${end}`;
            } else if (type === 'events') {
                url = `/events/${stock}?start_date=${start}&end_date=${end}`;
            } else {
                url = `/alt_data/${stock}`;
            }

            document.getElementById('result').textContent = 'Loading...';
            document.getElementById('result_title').textContent = `${stock} — ${type}`;

            try {
                const res = await fetch(url);
                const data = await res.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch(e) {
                document.getElementById('result').textContent = 'Error: ' + e;
            }
        }
    </script>
</body>
</html>
"""        