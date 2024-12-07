#Author:Chandira janith sirilal
#Date:2024.11.20
#Student ID:W2121265

# Task A: Input Validation

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
    choice  = None
    
    choice = input("Do you want to load another data set ? (Y / N) :")
    choice = choice.upper()
    if choice == "Y" :
        main()
    else:
        print ("Task successfully done. please check the result.txt for output result")
        
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
    filename = f'traffic_data{input_date}.csv'
    try:
        full_path = folder_path + '/' + filename
        with open(full_path, mode='r', encoding='utf-8') as file:
            csv_file = full_path
    except FileNotFoundError:
        print(f"Error: No file found for the date {input_date}")
        return
    
    # Manual CSV reading without CSV module
    def read_csv_manually(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            # Read header
            header = file.readline().strip().split(',')
            # Read data rows
            rows = [line.strip().split(',') for line in file]
        return header, rows
    
    # Read the file
    headers, data_rows = read_csv_manually(csv_file)
    
    # Create dictionary for easier access
    def create_dict_rows(headers, rows):
        dict_rows = []
        for row in rows:
            row_dict = {}
            for i, header in enumerate(headers):
                row_dict[header] = row[i]
            dict_rows.append(row_dict)
        return dict_rows
    
    rows = create_dict_rows(headers, data_rows)
    
    # Initialize counters
    total_vehicles = 0
    total_trucks = 0
    electric_hybrid = 0
    two_wheeled = 0
    busses_leaving_Elm_Avenue_Rabbit = 0
    vehicles_no_turning = 0
    percentage_trucks = 0
    total_bicycle = 0
    over_spead_limit = 0
    total_Elm_Avenue_Rabbit_Road = 0
    total_hanley_highway_westway = 0
    total_sctr_rabbitRoad = 0
    percentage_of_sctr_rabbit = 0
    vehicles_by_hour = {}
    rain_time = 0  
    rain_times = []
    previous_time = None
    
 
    def parse_time(time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    
    # Iterate over each row and count based on conditions
    for row in rows:
        total_vehicles += 1
        if row['VehicleType'].strip().lower() == 'truck':
            total_trucks += 1
        if row.get('elctricHybrid', '').strip().lower() == 'true':
            electric_hybrid += 1
        if row.get('VehicleType', '').strip().lower() in ['bicycle', 'motorcycle', 'scooter']:
            two_wheeled += 1
        if (row.get('VehicleType', '').strip().lower() == 'buss' and 
            row.get('JunctionName', '').strip().lower() == 'elm avenue/rabbit road' and 
            row.get('travel_Direction_out', '').strip().lower() == 'n'):
            busses_leaving_Elm_Avenue_Rabbit += 1
        if (row.get('travel_Direction_in', '').strip().lower() == 
            row.get('travel_Direction_out', '').strip().lower()):
            vehicles_no_turning += 1
        
        if row.get('VehicleType', '').strip().lower() == 'bicycle':
            total_bicycle += 1
        
        if int(row.get('JunctionSpeedLimit', 0)) < int(row.get('VehicleSpeed', 0)):
            over_spead_limit += 1
        
        if row.get('JunctionName', '').strip().lower() == 'elm avenue/rabbit road':
            total_Elm_Avenue_Rabbit_Road += 1
        
        if row.get('JunctionName', '').strip().lower() == 'hanley highway/westway':
            total_hanley_highway_westway += 1
        
        if (row.get('JunctionName', '').strip().lower() == 'elm avenue/rabbit road' and 
            row.get('VehicleType', '').strip().lower() == 'scooter'):
            total_sctr_rabbitRoad += 1
        
        # Manual hour tracking
        if row.get('JunctionName', '').strip().lower() == 'hanley highway/westway':
            hour = row.get('timeOfDay', '').split(':')[0]
            vehicles_by_hour[hour] = vehicles_by_hour.get(hour, 0) + 1
        
      
        # Manual rain time calculation
        weather = row.get('Weather_Conditions', '').strip().lower()
        if weather in ['light rain', 'heavy rain']:
            current_time = parse_time(row.get('timeOfDay', '00:00:00'))
            rain_times.append(current_time)
            if previous_time is not None:
                # Calculate time difference in seconds
                rain_time += current_time - previous_time if current_time >= previous_time else 0
            previous_time = current_time
        else:
            previous_time = None

    # Sort the rain times in ascending order
    rain_times.sort()

    # Recalculate the total rain duration
    total_rain_hours = 0
    total_rain_minutes = 0
    if rain_times:
        start_time = rain_times[0]
        end_time = rain_times[-1]
        total_rain_seconds = end_time - start_time
        total_rain_hours = total_rain_seconds // 3600
        total_rain_minutes = (total_rain_seconds % 3600) // 60
    avg_bike_per_hour = round(total_bicycle / 24)
    percentage_trucks = round((total_trucks / total_vehicles) * 100)
    percentage_of_sctr_rabbit = round((total_Elm_Avenue_Rabbit_Road / total_sctr_rabbitRoad)) if total_sctr_rabbitRoad > 0 else 0
    
    # Find busiest hour
    busiest_hour = max(vehicles_by_hour, key=vehicles_by_hour.get) if vehicles_by_hour else '0'
    max_vehicles = vehicles_by_hour.get(busiest_hour, 0)
    endrange = int(busiest_hour) + 1
    
    # Results dictionary
    strtxt = "The Total number of"
    endtxt = "for this date"
    results = {
        "CSV File Selected": f"{csv_file}" ,
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
        "The highest number of vehicle in an hour  on Hanley Highway/Westway is ":f"{max_vehicles} vehicles",
        "The most vehicle through Hanley Highway/westway were recorded between " : f"{busiest_hour}:00 and {endrange}:00",
        "Total rain duration " : f"{int(total_rain_hours)} hours and {int(total_rain_minutes)} minutes."
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
        
    save_results_to_file(outcomes)


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    try:
        # Open the file in append mode
        with open(file_name, "a") as file:
            # Add a header to indicate a new set of results
            file.write("\n--- New Results ---\n")
            # Write each outcome key and value
            for key, value in outcomes.items():
                file.write(f"{key}: {value}\n")
            # Add a footer for better readability
            file.write("\n-------------------\n")
        print(f"Results successfully saved to {file_name}.")
    except Exception as e:
        print(f"An error occurred while saving results: {e}")
        
    validate_continue_input()

# if you have been contracted to do this assignment please do not remove this line

def main():
    folder_path = "c:/Users/ITS/OneDrive/Desktop/IIT docs/acadamic/SD/course work"
    day , month, year = validate_date_input()
    
    input_date= f"{day}{month}{year}"

    outcomes=process_csv_data(folder_path,input_date)
    display_outcomes(outcomes)
    
main()