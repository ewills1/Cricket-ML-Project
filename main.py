from app.train import TrainModel
from app.parse_json import ParseJson

def main(json_dir, csv_dir):
    # Parse JSON files and save to CSV
    parser = ParseJson(json_dir)
    parser.parse_json_files()
    
    # Train the model using the parsed data
    trainer = TrainModel(csv_dir)
    trainer.train_model()
    trainer.plot_results()

if __name__ == "__main__":
    # Directories for JSON and CSV files
    json_dir = "./data/ipl" 
    csv_dir = "./csv/" 

    main(json_dir, csv_dir)
