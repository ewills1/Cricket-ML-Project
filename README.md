This project is a machine learning model designed to predict the final score of T20 cricket matches, trained using Indian Premier League (IPL) data. T20 cricket is a dynamic and fast-paced format, making score prediction a complex task due to the non-linear and contextual nature of the game. This project leverages a Random Forest Regressor to model these complexities effectively.

This project also includes a Flask-API based backend, and a React frontend. 

The Flask backend provides a web server endpoint that serves the latest model predictions. These can be updated by adding a new set of matches into the /data directory, and updating the **json_dir** in main before running.

The React frontend uses a GET call to recieve the latest model predictions and display both a clear table of the predictions, and a plot of the predicted scores against the actual scores. 


Why Random Forest Regressor?

The Random Forest Regressor is particularly suited for this problem because:

 - It handles non-linear relationships well, which is crucial in cricket where runs and wickets do not follow a systematic pattern.
 - It is robust to overfitting, especially with limited or noisy data.
 - It can naturally handle both numerical and categorical features, making it versatile for including cricket-specific inputs like overs and game phases.

Features

The model uses the following features to make predictions:

- Cumulative Runs: The total runs scored by the team so far.
- Cumulative Wickets: The total wickets lost by the team so far.
- Current Run Rate: The average runs scored per over up to the current point in the match.
- Game Phases: Categorized into Powerplay (overs 0-6), Middle Overs (overs 7-15), and Death Overs (overs 16-20) to account for scoring  patterns specific to these phases.
- Remaining Overs and Wickets: Contextual information about how much of the game is left to play and resources remaining.

Model Performance

The model achieves the following performance metrics:

    Root Mean Squared Error (RMSE): 21.69
    - This means the predictions are, on average, 21.69 runs away from the actual final scores.

Potential Improvements

    Incorporate Contextual Match Features:
        Batting team's historical performance (e.g., average scores under similar conditions).
        Opponent team's strengths and weaknesses, particularly in bowling.
        Venue-specific data (e.g., average scores at the ground, pitch conditions).
        Weather and toss decisions.

    Explore Advanced Machine Learning Models:
        Implement Gradient Boosting algorithms like XGBoost, LightGBM, or CatBoost for better handling of tabular data and feature interactions.
        Experiment with Neural Networks to capture deeper and more complex relationships. While this approach would require a much larger dataset and more computational resources, it has the potential to significantly improve accuracy.