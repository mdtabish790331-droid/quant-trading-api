<h1 align="center">📈 Quant Trading Market Data API</h1>

<p align="center">
A production-grade <b>Market Data Pipeline + API System</b> for quantitative trading
</p>

<hr>

<h2>👨‍💻 Author</h2>
<p>
<b>Mohammad Danish (Dani)</b><br>
📅 April 2026<br>
🚀 Version: 2.0.0
</p>

<hr>

<h2>🧠 Project Overview</h2>
<ul>
<li>📊 Market Data Collection (OHLCV)</li>
<li>🏢 Fundamental Data</li>
<li>🌍 Macro Economic Indicators</li>
<li>📰 News & Events</li>
<li>🏭 Sector Intelligence</li>
<li>📈 Strategy Backtesting</li>
</ul>

<hr>

<h2>🏗️ System Architecture</h2>

<pre>
[Yahoo Finance / APIs]
          ↓
   Data Ingestion Layer
          ↓
     Validation Layer
          ↓
   PostgreSQL Database
          ↓
      FastAPI Backend
          ↓
   Backtesting Engine
</pre>

<hr>

<h2>⚙️ Setup Instructions</h2>

<h3>Step 1: Install Requirements</h3>

<pre>pip install -r requirements.txt</pre>

<h3>Step 2: Create .env file</h3>

<pre>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quant_trading
DB_USER=postgres
DB_PASSWORD=your_password_here
</pre>

<p>⚠️ Never upload <b>.env</b> to GitHub</p>

<h3>Step 3: Setup Database</h3>
<pre>python database.py</pre>

<h3>Step 4: Fetch Data</h3>
<pre>
python ingestion.py
python sectors_data.py
python fetch_fundamentals.py
python fetch_macro.py
python fetch_news.py
</pre>

<h3>Step 5: Validate Data</h3>
<pre>python validation.py</pre>

<h3>Step 6: Run API</h3>
<pre>uvicorn api:app --reload</pre>

<p>👉 Open: <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a></p>

<hr>

<h2>🌐 API Endpoints</h2>

<table>
<tr><th>Endpoint</th><th>Description</th></tr>
<tr><td>/</td><td>API Status</td></tr>
<tr><td>/stocks</td><td>Stock List</td></tr>
<tr><td>/prices/{stock}</td><td>Price Data</td></tr>
<tr><td>/events/{stock}</td><td>News & Events</td></tr>
<tr><td>/backtest/{stock}</td><td>Backtest</td></tr>
<tr><td>/sectors</td><td>Sector List</td></tr>
<tr><td>/sector/{name}</td><td>Sector Details</td></tr>
<tr><td>/alt_data/{stock}</td><td>Alt Data</td></tr>
<tr><td>/features/{stock}</td><td>All Features</td></tr>
<tr><td>/docs</td><td>Swagger UI</td></tr>
</table>

<hr>

<h2>📊 Data Coverage</h2>

<ul>
<li><b>Stocks:</b> Banking, IT, FMCG, Auto, Others</li>
<li><b>Data Types:</b> Market, Fundamentals, Macro, News, Sectors</li>
</ul>

<hr>

<h2>🗄️ Database Tables</h2>

<ul>
<li>prices</li>
<li>events</li>
<li>sectors</li>
<li>alt_data</li>
</ul>

<hr>

<h2>✅ Validation Rules</h2>

<ul>
<li>High ≥ Open & Close</li>
<li>Low ≤ Open & Close</li>
<li>Volume ≥ 0</li>
<li>No NULL values</li>
<li>No duplicates</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
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
└── README.md
</pre>

<hr>

<h2>🧪 Run Tests</h2>

<pre>python test/test_pipeline.py</pre>

<hr>

<h2>📤 Export CSV</h2>

<pre>python export_csv.py</pre>

<hr>

<h2>🔒 Security</h2>

<ul>
<li>No hardcoded credentials</li>
<li>Uses .env file</li>
<li>.env ignored in git</li>
</ul>

<hr>

<h2>🚀 Future Improvements</h2>

<ul>
<li>Live data streaming</li>
<li>Machine Learning models</li>
<li>Risk management</li>
<li>Frontend dashboard</li>
</ul>

<hr>

<h2>💡 Highlights</h2>

<ul>
<li>✔ End-to-end pipeline</li>
<li>✔ Real-world architecture</li>
<li>✔ Backtesting engine</li>
<li>✔ API ready</li>
</ul>