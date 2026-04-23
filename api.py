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
    <title>Quant Trading API Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial; background: #f5f5f5; color: #333; }
        .navbar { background: #1a1a2e; color: white; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between; }
        .navbar h1 { font-size: 20px; }
        .navbar span { font-size: 12px; background: #16213e; padding: 4px 10px; border-radius: 20px; }
        .container { max-width: 900px; margin: 30px auto; padding: 0 20px; }
        .tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
        .tab { padding: 8px 18px; border-radius: 20px; border: none; cursor: pointer; font-size: 13px; background: white; border: 1px solid #ddd; color: #555; }
        .tab.active { background: #1a1a2e; color: white; border-color: #1a1a2e; }
        .card { background: white; border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .card h3 { margin-bottom: 16px; font-size: 16px; color: #1a1a2e; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; }
        .form-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
        .form-group { flex: 1; min-width: 150px; }
        label { display: block; font-size: 12px; font-weight: bold; color: #666; margin-bottom: 6px; }
        input, select { width: 100%; padding: 9px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 13px; }
        input:focus, select:focus { outline: none; border-color: #1a1a2e; }
        .btn { background: #1a1a2e; color: white; padding: 10px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; width: 100%; margin-top: 4px; }
        .btn:hover { background: #16213e; }
        .btn-sm { background: #007bff; padding: 6px 14px; border: none; border-radius: 4px; color: white; cursor: pointer; font-size: 12px; margin: 2px; }
        .result-box { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 16px; font-family: monospace; font-size: 12px; max-height: 400px; overflow-y: auto; white-space: pre-wrap; margin-top: 16px; }
        .stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px; }
        .stat { background: white; border-radius: 10px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .stat-num { font-size: 28px; font-weight: bold; color: #1a1a2e; }
        .stat-label { font-size: 12px; color: #888; margin-top: 4px; }
        .stock-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; }
        .stock-btn { padding: 8px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; font-size: 12px; text-align: center; }
        .stock-btn:hover { background: #1a1a2e; color: white; }
        .section { display: none; }
        .section.active { display: block; }
        .loading { color: #888; font-style: italic; }
        .error { color: #dc3545; }
        .success { color: #28a745; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; background: #e8f4fd; color: #007bff; margin: 2px; }
    </style>
</head>
<body>

<div class="navbar">
    <h1>📈 Quant Trading API</h1>
    <span>v2.0.0 — Live</span>
</div>

<div class="container">

    <div class="stats-row">
        <div class="stat"><div class="stat-num">20</div><div class="stat-label">Stocks</div></div>
        <div class="stat"><div class="stat-num">187</div><div class="stat-label">Sectors</div></div>
        <div class="stat"><div class="stat-num">9</div><div class="stat-label">Endpoints</div></div>
        <div class="stat"><div class="stat-num">&lt;200ms</div><div class="stat-label">Latency</div></div>
    </div>

    <div class="tabs">
        <button class="tab active" onclick="showSection('prices')">📊 Price Data</button>
        <button class="tab" onclick="showSection('events')">📰 Events</button>
        <button class="tab" onclick="showSection('altdata')">🔬 Alt Data</button>
        <button class="tab" onclick="showSection('sectors')">🏭 Sectors</button>
        <button class="tab" onclick="showSection('backtest')">⚡ Backtest</button>
        <button class="tab" onclick="showSection('stocks')">📋 All Stocks</button>
    </div>

    <!-- PRICES -->
    <div class="section active" id="section-prices">
        <div class="card">
            <h3>📊 Price Data — OHLCV</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Stock</label>
                    <select id="p-stock">
                        <option>RELIANCE.NS</option><option>TCS.NS</option>
                        <option>HDFCBANK.NS</option><option>INFY.NS</option>
                        <option>HINDUNILVR.NS</option><option>ICICIBANK.NS</option>
                        <option>SBIN.NS</option><option>BHARTIARTL.NS</option>
                        <option>KOTAKBANK.NS</option><option>LT.NS</option>
                        <option>AXISBANK.NS</option><option>WIPRO.NS</option>
                        <option>HCLTECH.NS</option><option>ASIANPAINT.NS</option>
                        <option>MARUTI.NS</option><option>TITAN.NS</option>
                        <option>SUNPHARMA.NS</option><option>ULTRACEMCO.NS</option>
                        <option>BAJFINANCE.NS</option><option>ITC.NS</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="date" id="p-start" value="2024-01-01">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="date" id="p-end" value="2024-12-31">
                </div>
            </div>
            <button class="btn" onclick="fetchPrices()">Fetch Price Data</button>
            <div class="result-box" id="p-result">Results will appear here...</div>
        </div>
    </div>

    <!-- EVENTS -->
    <div class="section" id="section-events">
        <div class="card">
            <h3>📰 Events & News</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Stock</label>
                    <select id="e-stock">
                        <option>RELIANCE.NS</option><option>TCS.NS</option>
                        <option>HDFCBANK.NS</option><option>INFY.NS</option>
                        <option>HINDUNILVR.NS</option><option>ICICIBANK.NS</option>
                        <option>SBIN.NS</option><option>BHARTIARTL.NS</option>
                        <option>KOTAKBANK.NS</option><option>LT.NS</option>
                        <option>AXISBANK.NS</option><option>WIPRO.NS</option>
                        <option>HCLTECH.NS</option><option>ASIANPAINT.NS</option>
                        <option>MARUTI.NS</option><option>TITAN.NS</option>
                        <option>SUNPHARMA.NS</option><option>ULTRACEMCO.NS</option>
                        <option>BAJFINANCE.NS</option><option>ITC.NS</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="date" id="e-start" value="2024-01-01">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="date" id="e-end" value="2024-12-31">
                </div>
            </div>
            <button class="btn" onclick="fetchEvents()">Fetch Events</button>
            <div class="result-box" id="e-result">Results will appear here...</div>
        </div>
    </div>

    <!-- ALT DATA -->
    <div class="section" id="section-altdata">
        <div class="card">
            <h3>🔬 Alternative Data</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Stock</label>
                    <select id="a-stock">
                        <option>RELIANCE.NS</option><option>TCS.NS</option>
                        <option>HDFCBANK.NS</option><option>INFY.NS</option>
                        <option>HINDUNILVR.NS</option><option>ICICIBANK.NS</option>
                        <option>SBIN.NS</option><option>BHARTIARTL.NS</option>
                        <option>KOTAKBANK.NS</option><option>LT.NS</option>
                        <option>AXISBANK.NS</option><option>WIPRO.NS</option>
                        <option>HCLTECH.NS</option><option>ASIANPAINT.NS</option>
                        <option>MARUTI.NS</option><option>TITAN.NS</option>
                        <option>SUNPHARMA.NS</option><option>ULTRACEMCO.NS</option>
                        <option>BAJFINANCE.NS</option><option>ITC.NS</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Feature (optional)</label>
                    <select id="a-feature">
                        <option value="">All Features</option>
                        <option>pe_ratio</option>
                        <option>eps</option>
                        <option>revenue</option>
                        <option>ebitda</option>
                        <option>market_cap</option>
                        <option>profit_margin</option>
                        <option>return_on_equity</option>
                        <option>news_count</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="fetchAltData()">Fetch Alt Data</button>
            <div class="result-box" id="a-result">Results will appear here...</div>
        </div>
    </div>

    <!-- SECTORS -->
    <div class="section" id="section-sectors">
        <div class="card">
            <h3>🏭 Sectors</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Search Sector</label>
                    <input type="text" id="s-search" placeholder="e.g. IT, Banking, Pharma...">
                </div>
            </div>
            <div style="display:flex; gap:8px;">
                <button class="btn" style="flex:1" onclick="fetchSectors()">All Sectors</button>
                <button class="btn" style="flex:1; background:#007bff" onclick="searchSector()">Search Sector</button>
            </div>
            <div class="result-box" id="s-result">Results will appear here...</div>
        </div>
    </div>

    <!-- BACKTEST -->
    <div class="section" id="section-backtest">
        <div class="card">
            <h3>⚡ Backtest Strategy</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Stock</label>
                    <select id="b-stock">
                        <option>RELIANCE.NS</option><option>TCS.NS</option>
                        <option>HDFCBANK.NS</option><option>INFY.NS</option>
                        <option>HINDUNILVR.NS</option><option>ICICIBANK.NS</option>
                        <option>SBIN.NS</option><option>BHARTIARTL.NS</option>
                        <option>KOTAKBANK.NS</option><option>LT.NS</option>
                        <option>AXISBANK.NS</option><option>WIPRO.NS</option>
                        <option>HCLTECH.NS</option><option>ASIANPAINT.NS</option>
                        <option>MARUTI.NS</option><option>TITAN.NS</option>
                        <option>SUNPHARMA.NS</option><option>ULTRACEMCO.NS</option>
                        <option>BAJFINANCE.NS</option><option>ITC.NS</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="fetchBacktest()">Run Backtest</button>
            <div class="result-box" id="b-result">Results will appear here...</div>
        </div>
    </div>

    <!-- ALL STOCKS -->
    <div class="section" id="section-stocks">
        <div class="card">
            <h3>📋 All Stocks</h3>
            <button class="btn" onclick="fetchAllStocks()">Load All Stocks</button>
            <div class="result-box" id="st-result">Results will appear here...</div>
        </div>
    </div>

</div>

<script>
const BASE = '';

function showSection(name) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('section-' + name).classList.add('active');
    event.target.classList.add('active');
}

async function callAPI(url, resultId) {
    const box = document.getElementById(resultId);
    box.textContent = 'Loading...';
    box.className = 'result-box loading';
    try {
        const res = await fetch(url);
        const data = await res.json();
        box.textContent = JSON.stringify(data, null, 2);
        box.className = 'result-box';
    } catch(e) {
        box.textContent = 'Error: ' + e;
        box.className = 'result-box error';
    }
}

function fetchPrices() {
    const stock = document.getElementById('p-stock').value;
    const start = document.getElementById('p-start').value;
    const end = document.getElementById('p-end').value;
    callAPI(`/prices/${stock}?start_date=${start}&end_date=${end}`, 'p-result');
}

function fetchEvents() {
    const stock = document.getElementById('e-stock').value;
    const start = document.getElementById('e-start').value;
    const end = document.getElementById('e-end').value;
    callAPI(`/events/${stock}?start_date=${start}&end_date=${end}`, 'e-result');
}

function fetchAltData() {
    const stock = document.getElementById('a-stock').value;
    const feature = document.getElementById('a-feature').value;
    const url = feature ? `/alt_data/${stock}?feature=${feature}` : `/alt_data/${stock}`;
    callAPI(url, 'a-result');
}

function fetchSectors() {
    callAPI('/sectors', 's-result');
}

function searchSector() {
    const q = document.getElementById('s-search').value;
    if (!q) { fetchSectors(); return; }
    callAPI(`/sector/${q}`, 's-result');
}

function fetchBacktest() {
    const stock = document.getElementById('b-stock').value;
    callAPI(`/backtest/${stock}`, 'b-result');
}

function fetchAllStocks() {
    callAPI('/stocks', 'st-result');
}
</script>
</body>
</html>
"""