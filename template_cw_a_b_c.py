#Author:
#Date:2024.11.20
#Student ID:W2121265

# Task A: Input Validation

import csv
import os
from collections import defaultdict

def validate_date_input():
    
    day = None
    month = None
    year = None
    
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
   
   # Get valid day input
    while day is None:
        day = input("Please enter the day of the survey in the format dd: ").strip()
        if not day.isdigit():
            print("Integer required  ")
            day = None
        elif int(day) < 1 or int(day) > 31:
            print("Out of range - values must be in the range 1 and 31. ")
            day = None

    # Get valid month input
    while month is None:
        month = input("Please enter the month of the survey in the format MM: ").strip()
        if not month.isdigit():
            print("Integer required  ")
            month = None
        elif int(month) < 1 or int(month) > 12:
            print("Out of range - values must be in the range 1 to 12.")
            month = None

    # Get valid year input
    while year is None:
        year = input("Please enter the year of the survey in the format YYYY: ").strip()
        if not year.isdigit():
            print("Integer required ")
            year = None
        elif int(year) < 2000 or int(year) > 2024:
            print("Out of range - values must range from 2000 to 2024.")
            year = None
    
    # Return the date in DD/MM/YYYY format
    return day, month, year

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    


# Task B: Processed Outcomes
def process_csv_data(folder_path,input_date):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    
  
    
    csv_file = None
    for filename in os.listdir(folder_path):
        if filename.endswith(f"{input_date}.csv"):
            csv_file = os.path.join(folder_path, filename)
            #print (f"the data file selected is {csv_file} ")
            break
    # If no file is found, print an error and return
    if csv_file is None:
        print(f"Error: No file found for the date {input_date}")
        return
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file) 
        
        # Initialize counters
        total_vehicles = 0
        total_trucks = 0
        electric_hybrid = 0
        two_wheeled = 0
        busses_leaving_Elm_Avenue_Rabbit =0
        vehicles_no_turning =0
        percentage_trucks = 0
        total_bicycle = 0
        over_spead_limit=0
        total_Elm_Avenue_Rabbit_Road =0
        total_hanley_highway_westway = 0
        total_sctr_rabbitRoad = 0
        none=""
        percentage_of_sctr_rabbit = 0
        vehicles_by_hour = defaultdict(int)
        
        
        # Iterate over each row and count based on conditions
        for row in reader:
            total_vehicles += 1
            if row['VehicleType'].strip().lower() == 'truck':
                total_trucks += 1
            if row.get('elctricHybrid').strip().lower() == 'true':
                electric_hybrid += 1
            if row.get('VehicleType').strip().lower() in ['bicycle', 'motorcycle', 'scooter']:
                two_wheeled += 1
            if row.get('VehicleType').strip().lower() == 'buss' and row.get('JunctionName').strip().lower() =='elm avenue/rabbit road' and row.get('travel_Direction_out').strip().lower() == 'n':
                busses_leaving_Elm_Avenue_Rabbit +=1
            if row.get('travel_Direction_in').strip().lower() == row.get('travel_Direction_out').strip().lower():
                vehicles_no_turning += 1
        
            
            if row.get('VehicleType').strip().lower() == 'bicycle':
                total_bicycle+=1
            
            
            if int (row.get('JunctionSpeedLimit')) < int( row.get('VehicleSpeed')):
                over_spead_limit+=1
                
            if row.get('JunctionName').strip().lower() == 'elm avenue/rabbit road':
                total_Elm_Avenue_Rabbit_Road +=1
                
            if row.get('JunctionName').strip().lower() == 'hanley highway/westway':
                total_hanley_highway_westway +=1
            
            if row.get('JunctionName').strip().lower() == 'elm avenue/rabbit road' and row.get('VehicleType').strip().lower() == 'scooter' :
                total_sctr_rabbitRoad +=1
                
            if row.get('JunctionName').strip().lower() == 'hanley highway/westway':
        # Extract hour from timeOfDay (e.g., '00:41:24' -> '00')
                hour = row.get('timeOfDay', '').split(':')[0]
                vehicles_by_hour[hour] += 1
                
                 
        avg_bike_per_hour = round (total_bicycle/24)
        percentage_trucks = round((total_trucks / total_vehicles) * 100) 
        percentage_of_sctr_rabbit = round((total_Elm_Avenue_Rabbit_Road / total_sctr_rabbitRoad))
        busiest_hour, max_vehicles = max(vehicles_by_hour.items(), key=lambda x: x[1])
      
                
    # Results dictionary to store the calculated outcomes
    strtxt = "The Total number of"
    endtxt= "for this date"
    results = {
        "CSV File Selected": csv_file,
        f"{strtxt} vehicles {endtxt}": total_vehicles,
        f"{strtxt} trucks {endtxt}": total_trucks,
        f"{strtxt} Electric Hybrid Vehicle{endtxt}": electric_hybrid,
        f"{strtxt} Two wheeled vehicle {endtxt}": two_wheeled,
        f"{strtxt} Busses leaving Elm Avenue/Rabbit Road heading North is " :busses_leaving_Elm_Avenue_Rabbit,
        f"{strtxt} vehicle through both junction not turning left or right is " :vehicles_no_turning,
        "Percentage of all vehicles recorded that are trucks" : f"{percentage_trucks}%",
        f"Average number of bicycles per hour {endtxt}" : f"{avg_bike_per_hour}",
        f"{strtxt} vehicle recorded as over the speed limit {endtxt} " : over_spead_limit,
        f"{strtxt} vehicles records through Elm Avenue Rabbit Round junction is " : total_Elm_Avenue_Rabbit_Road,
        f"{strtxt} vehicles records through Hanley Highway/Westway junction is " : total_hanley_highway_westway,
        f"{strtxt} of vehicles recorded through Elm Avenue Rabbit Round are scooter ": f"{percentage_of_sctr_rabbit}%",
        f"The peak hour on Hanley Highway/Westway is {busiest_hour}:00 with":f"{max_vehicles} vehicles"
        
    }

    # Return the results dictionary
    return results
    
def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    if outcomes is None:
        print("No outcomes to display.")
        return 
    
    # Loop through and print the results in a formatted way
    for key, value in outcomes.items():
        print(f"{key}: {value}")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    pass  # File writing logic goes here

# if you have been contracted to do this assignment please do not remove this line

def main():
    folder_path = input("Enter the folder path containing the CSV files: ")
    day , month, year = validate_date_input()
    
    input_date= f"{day}{month}{year}"

    outcomes=process_csv_data(folder_path,input_date)
    display_outcomes(outcomes)
    
main()