# Cricket Score Predictor

This project is a machine learning model designed to predict the final score of T20 cricket matches, trained using Indian Premier League (IPL) data. T20 cricket is a dynamic and fast-paced format, making score prediction a complex task due to the non-linear and contextual nature of the game. This project leverages an XGBoost Regressor to model these complexities effectively.

## Project Overview

This project includes:

- A **Flask-based backend** that provides a web server endpoint serving the latest model predictions.
- A **React frontend** that retrieves and displays predictions in both a tabular format and as a graphical plot.
- A **machine learning model** trained on IPL data to estimate final match scores.

The latest predictions can be updated by adding new match data into the `/data` directory, updating the `json_dir` in `main.py`, and running the script to process and train the model.

## Why XGBoost Regressor?

XGBoost is chosen for this problem because:

- It efficiently handles large datasets and complex patterns in cricket data.
- It provides better generalization and higher accuracy compared to traditional methods.
- It supports feature importance analysis, helping understand key contributors to score prediction.

## Features Used

The model uses the following features for prediction:

- **Cumulative Runs**: The total runs scored by the team so far.
- **Cumulative Wickets**: The total wickets lost by the team so far.
- **Current Run Rate**: The average runs scored per over up to the current point in the match.
- **Game Phases**: Categorized into Powerplay (overs 0-6), Middle Overs (overs 7-15), and Death Overs (overs 16-20) to account for phase-specific scoring patterns.
- **Remaining Overs and Wickets**: Contextual information about how much of the game is left and the resources available.

## Model Performance

The model achieves the following performance metrics:

- **Root Mean Squared Error (RMSE):** 21.69
  - This means the predictions are, on average, 21.69 runs away from the actual final scores.

## Potential Improvements

### Incorporate Contextual Match Features
- Batting team's historical performance (e.g., average scores under similar conditions).
- Opponent team's strengths and weaknesses, particularly in bowling.
- Venue-specific data (e.g., average scores at the ground, pitch conditions).
- Weather and toss decisions.

### Explore Advanced Machine Learning Models
- Experiment with **Neural Networks** to capture deeper and more complex relationships. While this approach would require a larger dataset and more computational resources, it has the potential to significantly improve accuracy.

