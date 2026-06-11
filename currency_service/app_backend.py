from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# ── Expanded 8-Currency Matrix (Fixes the 0.0000 display bug) ─────────────────
EXCHANGE_RATES = {
    "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 156.50, "CAD": 1.37, "CHF": 0.89, "AUD": 1.51, "CNY": 7.25, "USD": 1.0},
    "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 170.10, "CAD": 1.49, "CHF": 0.96, "AUD": 1.64, "CNY": 7.89, "EUR": 1.0},
    "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 198.30, "CAD": 1.74, "CHF": 1.12, "AUD": 1.91, "CNY": 9.21, "GBP": 1.0},
    "JPY": {"USD": 0.0064, "EUR": 0.0059, "GBP": 0.0050, "CAD": 0.0088, "CHF": 0.0057, "AUD": 0.0096, "CNY": 0.046, "JPY": 1.0},
    "CAD": {"USD": 0.73, "EUR": 0.67, "GBP": 0.57, "JPY": 114.23, "CAD": 1.0, "CHF": 0.65, "AUD": 1.10, "CNY": 5.29},
    "CHF": {"USD": 1.12, "EUR": 1.04, "GBP": 0.89, "JPY": 175.40, "CAD": 1.54, "CHF": 1.0, "AUD": 1.69, "CNY": 8.13},
    "AUD": {"USD": 0.66, "EUR": 0.61, "GBP": 0.52, "JPY": 103.80, "CAD": 0.91, "CHF": 0.59, "AUD": 1.0, "CNY": 4.80},
    "CNY": {"USD": 0.14, "EUR": 0.13, "GBP": 0.11, "JPY": 21.60, "CAD": 0.19, "CHF": 0.12, "AUD": 0.21, "CNY": 1.0}
}

DB_FILE = "history.json"

def log_transaction(source, target, amount, result, rate):
    """Atomically appends transaction records to the flat-file ledger using Streamlit-compatible keys."""
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
    """Fallback index route to prevent 404 errors when opening the raw URL."""
    return jsonify({
        "status": "online",
        "service": "Currency Converter Matrix Engine Backend",
        "version": "2.1.0",
        "endpoints_available": {
            "conversion": "/api/convert?source=USD&target=EUR&amount=100",
            "history_ledger": "/api/history"
        }
    })


@app.route('/api/convert', methods=['GET'])
def convert_currency():
    """Processes incoming conversion requests and updates data maps."""
    source = request.args.get('source')
    target = request.args.get('target')
    amount_str = request.args.get('amount')

    if not source or not target or not amount_str:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        amount = float(amount_str)
    except ValueError:
        return jsonify({"error": "Invalid amount numeric value"}), 400

    # Safety check against the updated full matrix lookup tables
    if source not in EXCHANGE_RATES or target not in EXCHANGE_RATES[source]:
        return jsonify({"error": "Unsupported currency pair"}), 400

    rate = EXCHANGE_RATES[source][target]
    calculated = amount * rate

    # Back-end persistence trigger
    log_transaction(source, target, amount, calculated, rate)
    
    return jsonify({
        "from": source,
        "to": target,
        "amt": amount,
        "res": round(calculated, 2),
        "rate": rate
    })


@app.route('/api/history', methods=['GET', 'DELETE'])
def handle_history():
    """Handles viewing records (GET) and purges the transactional ledger file (DELETE)."""
    if request.method == 'DELETE':
        try:
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
            return jsonify({"status": "success", "message": "Ledger dropped"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete log file: {str(e)}"}), 500

    # GET Method logic
    if not os.path.exists(DB_FILE):
        return jsonify([])
    
    logs = []
    with open(DB_FILE, "r") as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line.strip()))
    return jsonify(list(reversed(logs)))

def main():
    """Main package entrypoint function to launch the Flask REST engine."""
    app.run(port=8000, debug=True)

if __name__ == '__main__':
    main()