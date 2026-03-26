from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Allowed functions
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
    "pow": pow
}

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    expr = data.get("expression")

    try:
        result = eval(expr, {"__builtins__": None}, allowed)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)