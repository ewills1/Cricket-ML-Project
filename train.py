import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor as rf
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib 
import os

import numpy as np

class TrainModel:
    def __init__(self, csv_dir):
        self.csv_dir = csv_dir
        self.all_data = []
        self.predictions = []

    def train_model(self):
        # Load CSV file
        file_path = os.path.join(self.csv_dir, "processed_data.csv")
        df = pd.read_csv(file_path)

        # Prepare feature set and target
        X = df[['cumulative_runs', 'cumulative_wickets', 'current_run_rate']]  # Features
        y = df['final_score']  # Target (final score)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = rf(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the model for flask api
        joblib.dump(model, "cricket_score_model.pkl")

        # Predict on test set
        y_pred = model.predict(X_test)

        # Evaluate model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f'Mean Squared Error: {mse}')
        print(f'RMSE: {rmse}')

        predictions = pd.DataFrame({
            'Team': df.loc[X_test.index, 'team'],
            'Opponent': df.loc[X_test.index, 'opponent'],
            'Actual Final Score': y_test,
            'Predicted Final Score': y_pred,
            'Over': df.loc[X_test.index, 'over']
        })

        # Save the DataFrame to a CSV file
        predictions.to_csv('./csv/final_score_predictions.csv', index=False)
        self.predictions = predictions

    def get_predictions(self):
        return self.predictions

    def plot_results(self):
        # Load predictions
        predictions = pd.read_csv('./csv/final_score_predictions.csv')

        # ---- PLOT: Actual vs Predicted Scores ----
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=predictions['Actual Final Score'], y=predictions['Predicted Final Score'], alpha=0.7, edgecolor=None)
        plt.plot([min(predictions['Actual Final Score']), max(predictions['Actual Final Score'])],
                 [min(predictions['Actual Final Score']), max(predictions['Actual Final Score'])], linestyle='--', color='red')
        plt.xlabel("Actual Final Score")
        plt.ylabel("Predicted Final Score")
        plt.title("Actual vs Predicted Final Score")
        plt.grid(True)
        plt.savefig("./app/static/prediction_plot.png", dpi=300, bbox_inches="tight")
        plt.close()



