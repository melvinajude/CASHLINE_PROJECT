from flask import Flask, request, jsonify
from flask_cors import CORS # This allows your HTML to talk to this Python script

app = Flask(__name__)
CORS(app) # Crucial: Without this, the browser will block the connection

@app.route('/analyze-freelancer', methods=['POST'])
def analyze_freelancer():
    # 1. Get data from the Frontend
    data = request.json
    income = data.get('income', 0)
    expenses = data.get('expenses', 0)
    days_late = data.get('days_late', 0)

    # 2. Logic: The "Brain" calculations
    # Liquidity Bridge
    bridge_needed = max(0, expenses - income)
    
    # Reliability Score Calculation (Decay Algorithm)
    reliability_score = max(0, round(10 - (days_late / 3), 1))
    
    # Tax Estimator (10% flat for demo)
    tax_estimate = round(income * 0.10, 2)

    # 3. Send the response back to the Frontend
    return jsonify({
        "status": "success",
        "bridge": bridge_needed,
        "score": reliability_score,
        "tax": tax_estimate,
        "recommendation": "High Risk" if reliability_score < 5 else "Safe"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)