from flask import Flask, render_template , request , jsonify

from sklearn.linear_model import LinearRegression

import numpy as np

app = Flask(__name__)

users = {
    "inam": {
        "balance": 1000,
        
        "transactions" : []
    }
}

def generate_ai_insight(transactions):
    withdraws = [t["amount"] for t in transactions if t["type"] == "withdraw"]

    if len(withdraws) < 2:
        return "Not enough data for AI prediction."
    
    x = np.array(range(len(withdraws))).reshape(-1,1)

    y = np.array(withdraws)



    model = LinearRegression()

    model.fit(x,y)

    next_pred = model.predict([[len(withdraws)]])[0]


    return f"predicted next spending: ${round(next_pred , 2)}"

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/get-user")

def get_user():
    user = users["inam"]

    insight = generate_ai_insight(user["transactions"])

    return jsonify({
        "balance": user["balance"],

        "transactions" : user["transactions"],

        "insight": insight
    })

@app.route("/deposite", methods=["POST"])

def deposite():
    amount = int(request.json["amount"])

    users["inam"]["balance"] += amount

    users["inam"]["transactions"].append({"type" : "deposite" , "amount": amount})

    return jsonify({"message": "ok"})

@app.route("/withdraw" , methods = ["POST"])

def withdraw():
    amount = int (request.json["amount"])

    if users["inam"]["balance"] < amount:
        return jsonify({"message": "Insufficient"}), 400
    
    users["inam"]["balance"] -= amount
    users["inam"]["transactions"].append({"type": "withdraw" , "amount": amount})

    return jsonify ({"message": "ok"})

if __name__ == "__main__":
    app.run(debug=True)