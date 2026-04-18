
markdown# 📈 Quant Trading Market Data API

A production-grade Market Data API and Alternative Data Infrastructure
for event-driven quantitative trading systems.

**Built by:** Mohammad Danish  
**Date:** April 2026  
**Version:** 2.0.0

---

## 🏗️ System Architecture
[Yahoo Finance / External Sources]
↓
[Ingestion Layer]
↓
[Validation Layer]
↓
[PostgreSQL Database]
↓
[FastAPI Layer]
↓
[Backtest / Valuation / Signal Fusion]

---

## ⚙️ Setup Instructions

### Step 1 — Requirements Install karo
```bash
pip install -r requirements.txt
```

### Step 2 — `.env` file banao
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quant_trading
DB_USER=postgres
DB_PASSWORD=your_password_here

### Step 3 — Database Setup
```bash
python database.py
```

### Step 4 — Data Fetch karo
```bash
python ingestion.py
python sectors_data.py
python fetch_fundamentals.py
python fetch_macro.py
python fetch_news.py
```

### Step 5 — Validate karo
```bash
python validation.py
```

### Step 6 — API Start karo
```bash
uvicorn api:app --reload
```

---

## 🌐 API Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /` | API Status | `/` |
| `GET /stocks` | 20 Stocks List | `/stocks` |
| `GET /prices/{stock}` | Price Data | `/prices/RELIANCE.NS?start_date=2024-01-01&end_date=2024-12-31` |
| `GET /events/{stock}` | Corporate Events + News | `/events/RELIANCE.NS?start_date=2024-01-01&end_date=2024-12-31` |
| `GET /backtest/{stock}` | Run Backtest | `/backtest/RELIANCE.NS` |
| `GET /sectors` | 187 Sectors List | `/sectors` |
| `GET /sector/{name}` | Sector Details | `/sector/IT` |
| `GET /alt_data/{stock}` | Alternative Data | `/alt_data/RELIANCE.NS` |
| `GET /features/{stock}` | All Features | `/features/RELIANCE.NS` |
| `GET /docs` | Interactive API Docs | `/docs` |

---

## 📊 Data Universe

### 20 Stocks — 5 Categories

| Category | Stocks |
|----------|--------|
| 🏦 Banking | HDFCBANK.NS, ICICIBANK.NS, SBIN.NS, KOTAKBANK.NS, AXISBANK.NS |
| 💻 IT | TCS.NS, INFY.NS, WIPRO.NS, HCLTECH.NS |
| 🏭 Conglomerate | RELIANCE.NS, ITC.NS, LT.NS |
| 🛒 FMCG & Consumer | HINDUNILVR.NS, TITAN.NS, ASIANPAINT.NS |
| 🚗 Auto & Others | MARUTI.NS, BAJFINANCE.NS, SUNPHARMA.NS, ULTRACEMCO.NS, BHARTIARTL.NS |

### 5 Data Categories (As per PDF)

| # | Category | Source | Status |
|---|----------|--------|--------|
| 1 | Market Data (OHLCV) | yfinance | ✅ |
| 2 | Fundamental Data | yfinance | ✅ |
| 3 | Macro Economic Data | yfinance | ✅ |
| 4 | News & Sentiment | yfinance | ✅ |
| 5 | Sector & Industry | Manual | ✅ |

### 187 Sectors
Full industry universe — all stored in PostgreSQL.

---

## 🗄️ Database Schema

### prices table
```sql
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    stock VARCHAR(20) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume BIGINT NOT NULL,
    UNIQUE(stock, datetime)
);
```

### events table
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    stock VARCHAR(20) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    raw_text TEXT NOT NULL
);
```

### sectors table
```sql
CREATE TABLE sectors (
    id SERIAL PRIMARY KEY,
    sector_name TEXT NOT NULL,
    industry_name TEXT NOT NULL,
    num_companies INT DEFAULT 0,
    median_pe FLOAT DEFAULT 0,
    sales_growth FLOAT DEFAULT 0,
    opm FLOAT DEFAULT 0,
    roce FLOAT DEFAULT 0,
    median_return FLOAT DEFAULT 0
);
```

### alt_data table
```sql
CREATE TABLE alt_data (
    id SERIAL PRIMARY KEY,
    stock TEXT NOT NULL,
    source TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    value FLOAT,
    datetime TIMESTAMP NOT NULL
);
```

---

## ✅ Validation Rules

- High ≥ max(Open, Close)
- Low ≤ min(Open, Close)
- Volume ≥ 0
- No NULL values
- No missing timestamps
- Duplicate detection for news

---

## 📁 Project Structure
QUANT_TRADING/
│
├── .env                      # Credentials (never share!)
├── requirements.txt          # Python dependencies
├── api.py                    # FastAPI endpoints
├── database.py               # DB connection + tables
├── ingestion.py              # Stock price data
├── fetch_fundamentals.py     # Fundamental data
├── fetch_macro.py            # Macro economic data
├── fetch_news.py             # News + duplicate detection
├── sectors_data.py           # 187 sectors
├── validation.py             # Data validation
├── logger.py                 # JSON logging
├── data_loader.py            # Load from DB
├── export_csv.py             # Export to CSV
│
├── utils/
│   └── strategy/
│       ├── moving_average.py
│       ├── indicators.py
│       └── backtest/
│           ├── engine.py
│           ├── metrics.py
│           └── run_backtest.py
│
├── test/
│   └── test_pipeline.py
│
└── sample_data/
├── prices.csv
└── events.csv

---

## 🔒 Security

- No hardcoded credentials
- All secrets in `.env` file
- `.env` in `.gitignore` — never committed

---

## 🧪 Tests

```bash
python test/test_pipeline.py
```

---

## 📤 CSV Export

```bash
python export_csv.py
```

---

## 📋 Sample API Response

```json
{
  "stock": "RELIANCE.NS",
  "total_rows": 248,
  "data": [
    {
      "stock": "RELIANCE.NS",
      "datetime": "2024-01-01",
      "open": 2500.0,
      "high": 2550.0,
      "low": 2480.0,
      "close": 2530.0,
      "volume": 5000000
    }
  ]
}
```

---

## 🔗 How Other Modules Use This API

| Module | Endpoints Used |
|--------|---------------|
| Valuation Delta | `/alt_data/{stock}`, `/features/{stock}` |
| Backtest Module | `/prices/{stock}` |
| Price Reaction | `/prices/{stock}`, `/events/{stock}` |
| Signal Fusion | `/prices/{stock}`, `/alt_data/{stock}`, `/sectors` |
| Execution & Order | `/prices/{stock}`, `/events/{stock}` |

GitHub par update karo:
git add .
git commit -m "Added README"
git push
