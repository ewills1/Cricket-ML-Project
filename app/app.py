from flask import Flask, request, jsonify
import os
import json
import pandas as pd

app = Flask(__name__)

@app.route('/predict-file', methods=['POST'])
def predict_file():
    try:
        print(f"Files in request: {request.files}")

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        print(f"Received file: {file.filename}")

        # Check if no file was selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Make sure the file is a JSON file
        if file and file.filename.endswith('.json'):
            filepath = "./uploaded_file.json"
            file.save(filepath)

            # Initialize list to hold all data
            all_data = []

            # Read the JSON file content
            with open(filepath, 'r') as f:
                data = json.load(f)

                # Assuming only one innings
                innings = data['innings'][0]
                overs = innings['overs']
                team = innings['team']
                all_teams = data['info']['teams']  # List of teams in this match
                opponent = [t for t in all_teams if t != team][0]
                venue = data['info']['venue']

                # Calculate the final score
                final_score = sum(
                    delivery['runs']['total']
                    for over in overs
                    for delivery in over['deliveries']
                )

                cumulative_runs = 0
                cumulative_wickets = 0

                # Process deliveries
                for over in overs:
                    over_number = over['over']
                    for delivery in over['deliveries']:

                        # Phase based on over number
                        if 0 <= over_number < 6:
                            phase = "Powerplay"
                        elif 6 <= over_number < 16:
                            phase = "Middle Overs"
                        else:
                            phase = "Death Overs"
                       
                        # Update cumulative stats
                        runs = delivery['runs']['total']
                        cumulative_runs += runs

                        if 'wickets' in delivery:
                            cumulative_wickets += 1

                        remaining_overs = 20 - over_number
                        remaining_wickets = 10 - cumulative_wickets

                        # Append the processed data to all_data
                        all_data.append({
                            'file_name': file.filename,
                            'team': team,
                            'opponent': opponent,
                            'venue': venue,
                            'over': over_number,
                            'phase': phase,
                            'cumulative_runs': cumulative_runs,
                            'cumulative_wickets': cumulative_wickets,
                            'current_run_rate': cumulative_runs / (over_number + 1 + 1e-6),
                            'remaining_overs': remaining_overs,
                            'remaining_wickets': remaining_wickets,
                            'final_score': final_score
                        })

            # Convert the processed data to DataFrame
            df = pd.DataFrame(all_data)

            # You can choose to return this DataFrame or a subset of it, or save it as a CSV
            output_filepath = "./processed_data.csv"
            df.to_csv(output_filepath, index=False)

            # Send the file location as response
            return jsonify({
                "message": "File received and processed successfully.",
                "data": df.to_dict(orient="records")
            }), 200
        

        return jsonify({"error": "Invalid file type, please upload a JSON file"}), 400

    except Exception as e:
        print(f"Error: {str(e)}")  # This will print any unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
