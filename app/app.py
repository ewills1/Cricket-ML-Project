import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add root directory
from flask import Flask, request, jsonify
import json
import pandas as pd
import joblib
from main import main # Importing the main function from main.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model = joblib.load("cricket_score_model.pkl")

def load_predictions():
    latest_csv = "./csv/final_score_predictions.csv"
    df = pd.read_csv(latest_csv)

    return df.to_dict(orient="records")  # Convert DataFrame to JSON

@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    """
    API Endpoint to return predictions.
    """
    predictions = load_predictions()
    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)
