import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load CSV file - replace path if needed
file_path = "./processed_data.csv"
df = pd.read_csv(file_path)

# Prepare feature set and target
X = df[['cumulative_runs', 'cumulative_wickets', 'current_run_rate']]  # Features
y = df['final_score']  # Target (final score)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

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
    'Actual Final Score': y_test,  # Actual final scores
    'Predicted Final Score': y_pred,  # Predicted final scores'Over': overs  # Optionally include the over number for reference
})

# Save the DataFrame to a CSV file
predictions.to_csv('final_score_predictions.csv', index=False)

print("Predictions saved to 'final_score_predictions.csv'")
