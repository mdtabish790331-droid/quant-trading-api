📈 Quant Trading Market Data API

A production-grade market data pipeline + API system built for
event-driven quantitative trading strategies.

👨‍💻 Author

Mohammad Danish (Dani)
📅 April 2026
🚀 Version: 2.0.0

🧠 Project Overview

This project builds a complete data pipeline + backend system for:

📊 Market Data Collection (OHLCV)
🏢 Fundamental Data
🌍 Macro Economic Indicators
📰 News & Events
🏭 Sector Intelligence
📈 Strategy Backtesting
🏗️ System Architecture
[Yahoo Finance / External APIs]
              ↓
       Data Ingestion Layer
              ↓
        Validation Layer
              ↓
      PostgreSQL Database
              ↓
         FastAPI Backend
              ↓
  Backtesting & Strategy Engine
⚙️ Setup Instructions
🔹 Step 1: Install Requirements
pip install -r requirements.txt
🔹 Step 2: Create .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quant_trading
DB_USER=postgres
DB_PASSWORD=your_password_here

⚠️ Never upload .env to GitHub

🔹 Step 3: Setup Database
python database.py
🔹 Step 4: Fetch Data
python ingestion.py
python sectors_data.py
python fetch_fundamentals.py
python fetch_macro.py
python fetch_news.py
🔹 Step 5: Validate Data
python validation.py
🔹 Step 6: Run API Server
uvicorn api:app --reload

👉 Open in browser:

http://127.0.0.1:8000/docs
🌐 API Endpoints
Endpoint	Description
/	API Status
/stocks	List of Stocks
/prices/{stock}	Historical Price Data
/events/{stock}	News & Events
/backtest/{stock}	Strategy Backtest
/sectors	Sector List
/sector/{name}	Sector Details
/alt_data/{stock}	Alternative Data
/features/{stock}	Combined Features
/docs	Swagger UI
📊 Data Coverage
🟢 Stocks Universe (20 Stocks)
Banking: HDFC, ICICI, SBI, Kotak, Axis
IT: TCS, Infosys, Wipro, HCL
FMCG: HUL, ITC, Titan
Auto: Maruti
Others: Reliance, LT, etc.
🟢 Data Types
Type	Description	Status
Market Data	OHLCV	✅
Fundamentals	PE, EPS, Revenue	✅
Macro Data	Gold, Oil, USD/INR	✅
News	Articles & Events	✅
Sectors	Industry Data	✅
🗄️ Database Schema
📌 prices
stock
datetime
open, high, low, close
volume
📌 events
stock
event_type
datetime
raw_text
📌 sectors
sector_name
industry_name
financial metrics
📌 alt_data
stock
source
feature_name
value
datetime
✅ Data Validation Rules
High ≥ Open & Close
Low ≤ Open & Close
Volume ≥ 0
No NULL values
No duplicate records
📁 Project Structure
QUANT_TRADING/
│
├── api.py
├── database.py
├── ingestion.py
├── fetch_fundamentals.py
├── fetch_macro.py
├── fetch_news.py
├── validation.py
├── logger.py
├── data_loader.py
├── export_csv.py
│
├── utils/
│   └── strategy/
│       ├── moving_average.py
│       └── backtest/
│           └── engine.py
│
├── test/
├── sample_data/
└── README.md
🧪 Run Tests
python test/test_pipeline.py
📤 Export Data
python export_csv.py
📌 Sample API Response
{
  "stock": "RELIANCE.NS",
  "total_rows": 248,
  "data": [
    {
      "datetime": "2024-01-01",
      "open": 2500,
      "high": 2550,
      "low": 2480,
      "close": 2530,
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
