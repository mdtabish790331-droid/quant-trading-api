import psycopg2
import sys
sys.path.append('..')

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="quant_trading",
        user="postgres",
        password="pass123"  # apna password
    )
    return conn

# ✅ Test 1 - Database connection
def test_database_connection():
    print("🧪 Test 1: Database Connection...")
    try:
        conn = get_connection()
        conn.close()
        print("✅ PASSED — Database connected!\n")
        return True
    except Exception as e:
        print(f"❌ FAILED — {e}\n")
        return False

# ✅ Test 2 - Tables exist karti hain
def test_tables_exist():
    print("🧪 Test 2: Tables Exist...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "prices" in tables, "prices table missing!"
        assert "events" in tables, "events table missing!"
        
        cursor.close()
        conn.close()
        print("✅ PASSED — Both tables exist!\n")
        return True
    except Exception as e:
        print(f"❌ FAILED — {e}\n")
        return False

# ✅ Test 3 - Data exist karta hai
def test_data_exists():
    print("🧪 Test 3: Data Exists in Prices Table...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM prices")
        count = cursor.fetchone()[0]
        
        assert count > 0, "No data in prices table!"
        
        cursor.close()
        conn.close()
        print(f"✅ PASSED — {count} rows found in prices!\n")
        return True
    except Exception as e:
        print(f"❌ FAILED — {e}\n")
        return False

# ✅ Test 4 - Data validation
def test_data_validation():
    print("🧪 Test 4: Data Validation Rules...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # High >= Open aur Close
        cursor.execute("""
            SELECT COUNT(*) FROM prices
            WHERE high < open OR high < close
        """)
        bad_high = cursor.fetchone()[0]
        
        # Low <= Open aur Close
        cursor.execute("""
            SELECT COUNT(*) FROM prices
            WHERE low > open OR low > close
        """)
        bad_low = cursor.fetchone()[0]
        
        # Volume >= 0
        cursor.execute("""
            SELECT COUNT(*) FROM prices
            WHERE volume < 0
        """)
        bad_volume = cursor.fetchone()[0]
        
        assert bad_high == 0, f"{bad_high} rows with invalid HIGH!"
        assert bad_low == 0, f"{bad_low} rows with invalid LOW!"
        assert bad_volume == 0, f"{bad_volume} rows with invalid VOLUME!"
        
        cursor.close()
        conn.close()
        print("✅ PASSED — All validation rules passed!\n")
        return True
    except Exception as e:
        print(f"❌ FAILED — {e}\n")
        return False

# ✅ Test 5 - API response format
def test_api_response_format():
    print("🧪 Test 5: API Response Format...")
    try:
        import urllib.request
        import json
        
        url = "http://127.0.0.1:8000/stocks"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        
        assert "total_stocks" in data, "total_stocks missing!"
        assert "stocks" in data, "stocks missing!"
        assert data["total_stocks"] > 0, "No stocks found!"
        
        print(f"✅ PASSED — API returning {data['total_stocks']} stocks!\n")
        return True
    except Exception as e:
        print(f"❌ FAILED — {e}\n")
        return False

# ✅ Saare tests run karo
def run_all_tests():
    print("=" * 50)
    print("🚀 RUNNING ALL TESTS")
    print("=" * 50 + "\n")
    
    results = []
    results.append(test_database_connection())
    results.append(test_tables_exist())
    results.append(test_data_exists())
    results.append(test_data_validation())
    results.append(test_api_response_format())
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ Some tests failed — check above!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()
