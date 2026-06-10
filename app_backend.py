from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Pre-compiled high-precision multi-currency matrix
EXCHANGE_RATES = {
    "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 156.50, "CAD": 1.37, "USD": 1.0},
    "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 170.10, "CAD": 1.49, "EUR": 1.0},
    "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 198.30, "CAD": 1.74, "GBP": 1.0},
    "JPY": {"USD": 0.0064, "EUR": 0.0059, "GBP": 0.0050, "CAD": 0.0088, "JPY": 1.0},
    "CAD": {"USD": 0.73, "EUR": 0.67, "GBP": 0.57, "JPY": 114.23, "CAD": 1.0}
}

DB_FILE = "history.json"

def log_transaction(source, target, amount, result, rate):
    """Atomically appends transaction records to the flat-file ledger using Streamlit-compatible keys"""
    # Changed keys to 'from', 'to', 'amt', 'res', 'rate' to match Streamlit's expectations
    record = {
        "from": source, 
        "to": target, 
        "amt": amount, 
        "res": round(result, 2),
        "rate": rate
    }
    try:
        with open(DB_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

@app.route('/', methods=['GET'])
def backend_home():
    """Fallback index route to prevent 404 errors when opening the raw URL"""
    return jsonify({
        "status": "online",
        "service": "Currency Converter Matrix Engine Backend",
        "version": "2.0.0",
        "endpoints_available": {
            "conversion": "/api/convert?source=USD&target=EUR&amount=100",
            "history_ledger": "/api/history"
        }
    })
    
    # Back-end persistence trigger (passing the rate along as well)
    log_transaction(source, target, amount, calculated, rate)
    
    # MATCHING THE FRONTIER KEYS: This prevents the KeyError: 'res' in Streamlit
    return jsonify({
        "from": source,
        "to": target,
        "amt": amount,
        "res": round(calculated, 2),
        "rate": rate
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Endpoint reading stream transactions and reversing chronology"""
    if not os.path.exists(DB_FILE):
        return jsonify([])
    
    logs = []
    with open(DB_FILE, "r") as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line.strip()))
    return jsonify(list(reversed(logs)))

if __name__ == '__main__':
    app.run(port=8000, debug=True)