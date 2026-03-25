from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    # This tells Flask: "Go into the 'templates' folder and show index.html"
    return render_template('index.html') 

# ... keep your other @app.route stuff here ...

app = Flask(__name__)
CORS(app)

# Dummy database (for hackathon)
users = []
transactions = []

# ---------------------------
# 1. Onboarding User Data
# ---------------------------
@app.route('/onboard', methods=['POST'])
def onboard():
    data = request.json
    
    user = {
        "name": data.get("name"),
        "income": data.get("income"),
        "expenses": data.get("expenses"),
        "goal": data.get("goal")
    }
    
    users.append(user)
    
    return jsonify({"message": "User onboarded", "user": user})


# ---------------------------
# 2. Add Transaction
# ---------------------------
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    data = request.json
    
    transaction = {
        "amount": data.get("amount"),
        "type": data.get("type"),
        "category": data.get("category")
    }
    
    transactions.append(transaction)
    
    return jsonify({"message": "Transaction added"})


# ---------------------------
# 3. Get Dashboard Data
# ---------------------------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    
    balance = total_income - total_expense
    
    return jsonify({
        "income": total_income,
        "expense": total_expense,
        "balance": balance
    })


# ---------------------------
# 4. Financial Stress Meter
# ---------------------------
@app.route('/stress', methods=['GET'])
def stress():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    if total_expense > total_income:
        level = "HIGH 🔴"
    elif total_expense > 0.7 * total_income:
        level = "MEDIUM 🟡"
    else:
        level = "LOW 🟢"

    return jsonify({"stress_level": level})


# ---------------------------
# Run Server
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
