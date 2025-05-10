# === File: app.py ===
from flask import Flask, request, render_template_string
import pandas as pd
import webbrowser
import threading

app = Flask(__name__)

# Load and clean CSV
df = pd.read_csv("HSN_SAC.csv")
df.columns = df.columns.str.strip()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HSN Code Validator</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        .container { background: #fff; padding: 20px; max-width: 500px; margin: auto; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        input[type=text] { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; }
        .result { margin-top: 15px; padding: 10px; background: #e0e0e0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>HSN Code Validator</h2>
        <form method="POST">
            <input type="text" name="hsn" placeholder="Enter HSN code" required>
            <button type="submit">Validate</button>
        </form>
        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        code = request.form["hsn"].strip()
        if not code.isdigit() or len(code) not in [2, 4, 6, 8]:
            result = f"[❌] Invalid format: {code} (must be numeric, 2/4/6/8 digits)"
        elif code in df["HSNCode"].astype(str).values:
            desc = df[df["HSNCode"].astype(str) == code]["Description"].values[0]
            result = f"[✅] {code} is valid. Description: {desc}"
        else:
            result = f"[❌] HSN Code {code} not found in master data."
    return render_template_string(HTML_TEMPLATE, result=result)

# Open browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
