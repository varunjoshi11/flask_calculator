from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Only allow digits, decimal points, spaces, parentheses, and basic operators
SAFE_EXPR = re.compile(r'^[0-9+\-*/().\s]+$')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')

    # Validate expression to avoid malicious input
    if not SAFE_EXPR.match(expression):
        return jsonify({'result': 'Error'}), 400

    try:
        # Safe evaluation context with no builtins
        result = eval(expression, {"__builtins__": None}, {})
        # Check if result is finite number
        if not isinstance(result, (int, float)) or result != result or result == float('inf') or result == float('-inf'):
            return jsonify({'result': 'Error'}), 400

        # Round result to avoid floating point quirks
        rounded_result = round(result, 8)
        return jsonify({'result': str(rounded_result)})
    except Exception:
        return jsonify({'result': 'Error'}), 400

if __name__ == '__main__':
    app.run(debug=True)
