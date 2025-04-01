import os
import json 
import pandas as pd

class ParseJson:
    def __init__(self, json_dir):
        self.json_dir = json_dir
        self.all_data = []

    def parse_json_files(self):
        for file_name in os.listdir(self.json_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.json_dir, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                    # Deliveries from innings (assuming only one inning)
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

                            self.all_data.append({
                                'file_name': file_name,
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
        df = pd.DataFrame(self.all_data)
        return df
