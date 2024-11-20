#Author:
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
   
    while day is None:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 and 31.")
                day = None  
        except ValueError:
            print("Integer required") 

    # Get valid month input
    while month is None:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if month < 1 or month > 12:
                print("Out of range - values must be in the range 1 to 12.")
                month = None  
        except ValueError:
            print("Integer required")  
            
            
    while year is None:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY "))
            if year < 2000 or year > 2024:
                print("Out of range - values must range from 2000 and 2024. ")
                year = None  
        except ValueError:
            print("Integer required")
            
   
    return day, month, year


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    


# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    pass  # Logic for processing data goes here

def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    pass  # Printing outcomes to the console


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    pass  # File writing logic goes here

# if you have been contracted to do this assignment please do not remove this line

def main():
    day, month, year =validate_date_input()
    print (f"{day}-{month}-{year}")
    
main()