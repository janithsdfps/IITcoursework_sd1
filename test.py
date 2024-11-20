import csv
from collections import defaultdict
from datetime import datetime

def process_traffic_data(csv_file, input_date):
    # Initialize variables to store counts
    total_vehicles = 0
    total_trucks = 0
    total_electric = 0
    two_wheeled_vehicles = 0
    buses_north_elm_avenue = 0
    no_turn_vehicles = 0
    vehicles_over_speed_limit = 0
    elm_avenue_vehicles = 0
    hanley_highway_vehicles = 0
    scooter_percentage_elm_avenue = 0
    peak_hour_data = defaultdict(int)
    rain_hours = 0
    elm_avenue_vehicles_only = 0
    hanley_highway_vehicles_only = 0
    total_bicycles = 0
    total_hours = 0
    
    # Speed limit (this could be adjusted based on actual data)
    speed_limit = 30
    
    # Read the CSV file
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Filter for the selected date
            if row['Date'] != input_date:
                continue
            
            # Increment the total vehicle count
            total_vehicles += 1
            
            # Check for specific vehicle types
            if row['Vehicle Type'].lower() == 'truck':
                total_trucks += 1
            if row['Electric Hybrid'].lower() == 'true':
                total_electric += 1
            if row['Vehicle Type'].lower() in ['bike', 'motorbike', 'scooter']:
                two_wheeled_vehicles += 1
            if row['Vehicle Type'].lower() == 'bus' and row['JunctionName'] == 'Elm Avenue/Rabbit Road' and row['Travel Direction out'].lower() == 'n':
                buses_north_elm_avenue += 1
            
            # Check for vehicles without turning left or right
            if row['Travel Direction in'] == 'S' and row['Travel Direction out'] == 'S':
                no_turn_vehicles += 1
            
            # Check for vehicles over the speed limit
            if int(row['Vehicle Speed']) > speed_limit:
                vehicles_over_speed_limit += 1
            
            # Count vehicles passing through Elm Avenue and Hanley Highway junctions
            if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                elm_avenue_vehicles += 1
                if row['Vehicle Type'].lower() == 'scooter':
                    elm_avenue_vehicles_only += 1
            if row['JunctionName'] == 'Hanley Highway/Westway':
                hanley_highway_vehicles += 1
                if row['Vehicle Type'].lower() == 'scooter':
                    hanley_highway_vehicles_only += 1
            
            # Track the peak traffic hour
            hour = int(row['timeOfDay'].split(':')[0])
            peak_hour_data[hour] += 1
            
            # Track rain hours
            if row['Weather Conditions'].lower() == 'rain':
                rain_hours += 1
            
            # Track bicycles
            if row['Vehicle Type'].lower() == 'bike':
                total_bicycles += 1
                total_hours += 1  # Assuming bikes are reported hourly
    
    # Calculate percentage of trucks
    truck_percentage = (total_trucks / total_vehicles) * 100 if total_vehicles else 0
    
    # Calculate the average number of bicycles per hour
    average_bicycles_per_hour = total_bicycles // total_hours if total_hours else 0
    
    # Calculate peak hour
    peak_hour_count = max(peak_hour_data.values(), default=0)
    peak_hours = [hour for hour, count in peak_hour_data.items() if count == peak_hour_count]
    peak_hour_time = [f"Between {hour}:00 and {hour+1}:00" for hour in peak_hours]
    
    # Calculate scooter percentage for Elm Avenue
    scooter_elm_avenue = (elm_avenue_vehicles_only / elm_avenue_vehicles) * 100 if elm_avenue_vehicles else 0
    
    # Prepare the results
    results = {
        "CSV File": csv_file,
        "Total Vehicles": total_vehicles,
        "Total Trucks": total_trucks,
        "Total Electric Vehicles": total_electric,
        "Two Wheeled Vehicles": two_wheeled_vehicles,
        "Buses Heading North (Elm Avenue)": buses_north_elm_avenue,
        "No Turn Vehicles": no_turn_vehicles,
        "Truck Percentage": round(truck_percentage),
        "Average Bicycles per Hour": average_bicycles_per_hour,
        "Vehicles Over Speed Limit": vehicles_over_speed_limit,
        "Elm Avenue Vehicles": elm_avenue_vehicles,
        "Hanley Highway Vehicles": hanley_highway_vehicles,
        "Scooter Percentage (Elm Avenue)": round(scooter_elm_avenue),
        "Peak Hour(s) on Hanley Highway/Westway": peak_hour_time,
        "Total Rain Hours": rain_hours,
    }
    
    # Print results
    for key, value in results.items():
        print(f"{key}: {value}")
    
    return results


# Example usage:
input_date = input("Enter the date (DD/MM/YYYY): ")  # Example: 25/06/2024
csv_file_path = "traffic_data25062024.csv"  # Replace with your actual CSV file path

process_traffic_data(csv_file_path, input_date)
