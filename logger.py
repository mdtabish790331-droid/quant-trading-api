import json
from datetime import datetime

LOG_FILE = "trading_system.log"

def log(level, message):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message
    }
    
    # Terminal mein print karo
    print(json.dumps(log_entry, indent=2))
    
    # File mein bhi save karo
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def log_info(message):
    log("INFO", message)

def log_error(message):
    log("ERROR", message)

def log_warning(message):
    log("WARNING", message)

if __name__ == "__main__":
    log_info("System started successfully")
    log_warning("This is a warning message")
    log_error("This is an error message")
    print("\n✅ Logger working! Check 'trading_system.log' file")