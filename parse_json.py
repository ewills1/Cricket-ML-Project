import os
import json 
import pandas as pd

json_dir = "./data/ipl"

all_data = []

for file_name in os.listdir(json_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(json_dir, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Deliveries from innings (assuming only one inning)
            innings = data['innings'][0]
            overs = innings['overs']
            team = innings['team']
            all_teams = data['info']['teams']  # List of teams in this match
            opponent = [t for t in all_teams if t != team][0]


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

                    all_data.append({
                        'file_name': file_name,
                        'team': team,
                        'opponent': opponent,
                        'over': over_number,
                        'phase': phase,
                        'cumulative_runs': cumulative_runs,
                        'cumulative_wickets': cumulative_wickets,
                        'current_run_rate': cumulative_runs / (over_number + 1 + 1e-6),
                        'final_score': final_score
                    })

# Convert to DataFrame
df = pd.DataFrame(all_data)


# # Group data by file
# grouped_data = df.groupby(['file_name', 'over']).agg({
#     'runs': 'sum',
#     'wicket': 'sum'
# }).reset_index()

# # Calculate cumulative stats for each file - could add run rates and player stats in here
# grouped_data['cumulative_runs'] = grouped_data.groupby('file_name')['runs'].cumsum()
# grouped_data['cumulative_wickets'] = grouped_data.groupby('file_name')['wicket'].cumsum()

# # Add run rate and predict final score
# grouped_data['current_run_rate'] = grouped_data['cumulative_runs'] / (grouped_data['over'] + 1e-6)

# match_overs = 20
# grouped_data['predicted_final_score'] = grouped_data['current_run_rate'] * match_overs

print(df)

df.to_csv('processed_data.csv', index=False)
