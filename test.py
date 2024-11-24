import pandas as pd
from collections import defaultdict

# Load the CSV file
file_path = 'traffic_data15062024.csv'  # Update with the correct path
traffic_data = pd.read_csv(file_path)

# Check the file name
csv_file_name = file_path.split('/')[-1]

# Initialize counters and variables
total_vehicles = len(traffic_data)
total_trucks = len(traffic_data[traffic_data['VehicleType'].str.lower() == 'truck'])

# Results
results = {
    "CSV File Name": csv_file_name,
    "Total Vehicles": total_vehicles,
    "Total Trucks": total_trucks
}

# Print results
for key, value in results.items():
    print(f"{key}: {value}")
