import csv

def sort_csv_by_time(input_file, output_file, time_column_name):
    """
    Sorts a CSV file by a specified time column in ascending order.
    
    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output sorted CSV file.
        time_column_name (str): The name of the column containing time values (e.g., 'timeOfDay').
    """
    # Open the input CSV file
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Read all rows into a list

        # Sort rows by time column
        sorted_rows = sorted(rows, key=lambda row: parse_time(row[time_column_name]))

        # Open the output CSV file
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()  # Write the header to the output file
            writer.writerows(sorted_rows)  # Write sorted rows

def parse_time(time_str):
    """
    Converts a time string (HH:MM:SS) to seconds since midnight.
    
    Args:
        time_str (str): Time in the format 'HH:MM:SS'.
    
    Returns:
        int: Total seconds since midnight.
    """
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds

# Example usage
input_file = 'traffic_data16062024.csv'
output_file = 'sorted_output.csv'
time_column_name = 'timeOfDay'

sort_csv_by_time(input_file, output_file, time_column_name)
