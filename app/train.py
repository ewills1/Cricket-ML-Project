import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from matplotlib import pyplot as plt
import seaborn as sns

class TrainModel:
    def __init__(self, csv_dir):
        self.csv_dir = csv_dir
        self.all_data = []
        self.predictions = None  # Set to None instead of []
        self.X = None  # Initialize as None
        self.y = None
        self.df = None
        self.model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

    def preprocess_data(self):
        """ Load and preprocess data """
        file_path = os.path.join(self.csv_dir, "processed_data.csv")
        self.df = pd.read_csv(file_path)

        # Prepare feature set and target
        self.X = self.df[['cumulative_runs', 'cumulative_wickets', 'current_run_rate']]
        self.y = self.df['final_score']

    def tune_hyperparameters(self):
        """ Tune hyperparameters using RandomizedSearchCV """

        param_dist = {
            'n_estimators': np.arange(50, 200, 50), 
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],  
            'max_features': ['sqrt', 'log2']  
        }


        random_search = RandomizedSearchCV(
            self.model, param_distributions=param_dist,
            n_iter=5, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
        )

        random_search.fit(self.X, self.y)
        self.model = random_search.best_estimator_
        print("Best Parameters:", random_search.best_params_)
        return random_search.best_params_

    def train_model(self):
        """ Train the model and save predictions """
        self.preprocess_data()  # Load data first!

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        # Save the model for Flask API
        joblib.dump(self.model, "cricket_score_model_xgb.pkl")
        print("Model saved as cricket_score_model_xgb.pkl")

        # Predict on test set
        y_pred = self.model.predict(X_test)

        # Evaluate model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f'Mean Squared Error: {mse}')
        print(f'RMSE: {rmse}')

        predictions = pd.DataFrame({
            'Team': self.df.loc[X_test.index, 'team'],
            'Opponent': self.df.loc[X_test.index, 'opponent'],
            'Actual Final Score': y_test,
            'Predicted Final Score': y_pred,
            'Over': self.df.loc[X_test.index, 'over']
        })

        # Sort first by Team, then by Over (to see a team’s innings in order)
        predictions = predictions.sort_values(by=['Team', 'Over'])

        # Save the DataFrame to a CSV file
        predictions.to_csv('./csv/final_score_predictions.csv', index=False)
        print("Predictions saved to final_score_predictions.csv")
        self.predictions = predictions
        
    def get_predictions(self):
        return self.predictions

    def plot_results(self):
        """ Plot Results of predictions"""
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



