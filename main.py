from train import TrainModel
from parse.parse_json import ParseJson

class Main:
    def __init__(self, json_dir, csv_dir):
        self.json_dir = json_dir
        self.csv_dir = csv_dir

    def run(self):
        # Parse JSON files and save to CSV
        parser = ParseJson(self.json_dir)
        parser.parse_json_files()
        
        # Train the model using the parsed data
        trainer = TrainModel(self.csv_dir)
        trainer.train_model()
        trainer.plot_results()

if __name__ == "__main__":
    # Directories for JSON and CSV files
    json_dir = "./data/ipl" 
    csv_dir = "./csv/" 
    

    main = Main(json_dir, csv_dir)
    main.run()