from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Safe functions
allowed = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "factorial": math.factorial,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "abs": abs,
    "round": round
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    expr = data.get("expression")

    try:
        result = eval(expr, {"__builtins__": None}, allowed)
        return jsonify({"result": result})
    except Exception:
        return jsonify({"error": "Invalid Expression"})

if __name__ == "__main__":
    app.run(debug=True)