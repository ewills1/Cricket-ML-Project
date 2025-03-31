import sys
import os
from flask import Flask, request, jsonify, send_file
import pandas as pd
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add root directory
from main import main # Importing the main function from main.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_predictions():
    latest_csv = "./csv/final_score_predictions.csv"
    df = pd.read_csv(latest_csv)

    return df.to_dict(orient="records")  # Convert DataFrame to JSON

@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    #API Endpoint to return predictions.
    predictions = load_predictions()
    return jsonify(predictions)

@app.route("/api/plot", methods=["GET"])
def get_plot():
    #API Endpoint to return plots
    plot_path = "./static/prediction_plot.png"
    return send_file(plot_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
