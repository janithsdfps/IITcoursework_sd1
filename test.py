import tkinter as tk
import csv
from typing import List, Dict
from collections import defaultdict

class HistogramApp:
    def __init__(self, traffic_data: List[Dict], date: str):
        """
        Initializes the histogram application with the traffic data and selected date.
        
        :param traffic_data: List of dictionaries containing traffic data
        :param date: Selected date for the histogram
        """
        self.traffic_data = traffic_data
        self.date = date
        
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title(f"Traffic Volume Histogram - {date}")
        
        # Canvas dimensions and margins
        self.canvas_width = 800
        self.canvas_height = 500
        self.margin = 50
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=self.canvas_width, 
            height=self.canvas_height
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Prepare data for histogram
        self.prepare_histogram_data()
    
    def prepare_histogram_data(self):
        """
        Processes and aggregates traffic data by hour and junction.
        """
        # Group data by hour
        self.hourly_data = defaultdict(lambda: defaultdict(int))
        
        for entry in self.traffic_data:
            # Extract hour from timeOfDay
            try:
                hour = int(entry['timeOfDay'].split(':')[0])
                junction = entry['JunctionName']
                vehicle_type = entry['VehicleType']
                
                # Count vehicles by junction and hour
                self.hourly_data[hour][junction] += 1
            except (KeyError, ValueError, IndexError):
                # Skip entries with invalid data
                continue
        
        # Calculate max value for scaling
        self.max_vehicles = max(
            sum(junctions.values()) 
            for junctions in self.hourly_data.values()
        ) if self.hourly_data else 1
    
    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars with volume labels.
        """
        # Clear any existing content
        self.canvas.delete('all')
        
        # Define plot area
        plot_width = self.canvas_width - 2 * self.margin
        plot_height = self.canvas_height - 2 * self.margin
        
        # Draw X and Y axes
        self.canvas.create_line(
            self.margin, self.canvas_height - self.margin, 
            self.canvas_width - self.margin, self.canvas_height - self.margin, 
            width=2
        )
        self.canvas.create_line(
            self.margin, self.canvas_height - self.margin, 
            self.margin, self.margin, 
            width=2
        )
        
        # Calculate bar width and spacing
        num_hours = 24
        bar_width = plot_width / (num_hours * 1.5)
        bar_spacing = plot_width / num_hours
        
        # Color palette for junctions
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan']
        
        # Draw bars for each hour and junction
        for hour, junctions in sorted(self.hourly_data.items()):
            x_offset = self.margin + hour * bar_spacing
            
            for i, (junction, vehicles) in enumerate(junctions.items()):
                # Scale height to fit canvas
                bar_height = (vehicles / self.max_vehicles) * (plot_height * 0.9)
                
                # Draw bar
                bar_coords = [
                    x_offset + i * bar_width, 
                    self.canvas_height - self.margin - bar_height,
                    x_offset + (i + 1) * bar_width, 
                    self.canvas_height - self.margin
                ]
                self.canvas.create_rectangle(
                    bar_coords[0], bar_coords[1],
                    bar_coords[2], bar_coords[3], 
                    fill=colors[i % len(colors)],
                    outline='black'
                )
                
                # Add volume label on top of the bar
                label_x = (bar_coords[0] + bar_coords[2]) / 2
                label_y = bar_coords[1] - 5  # 5 pixels above the bar
                self.canvas.create_text(
                    label_x, label_y, 
                    text=str(vehicles), 
                    anchor='s',
                    font=('Arial', 8)
                )
        
        # Add X-axis labels (hours)
        for hour in range(24):
            x = self.margin + hour * bar_spacing + bar_spacing / 2
            self.canvas.create_text(
                x, self.canvas_height - self.margin + 15, 
                text=str(hour), 
                anchor='n'
            )
        
        # Add Y-axis labels (vehicle count)
        y_label_count = 5
        for i in range(y_label_count + 1):
            y_value = int(self.max_vehicles * i / y_label_count)
            y = self.canvas_height - self.margin - (i / y_label_count) * plot_height
            self.canvas.create_text(
                self.margin - 10, y, 
                text=str(y_value), 
                anchor='e'
            )
        
        # Title
        self.canvas.create_text(
            self.canvas_width / 2, 
            self.margin / 2, 
            text=f"Traffic Volume by Hour - {self.date}", 
            font=('Arial', 12, 'bold')
        )
        
        # Y-axis label
        self.canvas.create_text(
            self.margin / 2, 
            self.canvas_height / 2, 
            text='Vehicle Count', 
            angle=90, 
            font=('Arial', 10)
        )
        
        # X-axis label
        self.canvas.create_text(
            self.canvas_width / 2, 
            self.canvas_height - 10, 
            text='Hour of Day', 
            font=('Arial', 10)
        )
    
    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Get unique junctions
        junctions = set(
            junction 
            for hour_data in self.hourly_data.values() 
            for junction in hour_data.keys()
        )
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan']
        
        for i, junction in enumerate(junctions):
            self.canvas.create_rectangle(
                self.canvas_width - 200, 
                self.margin + i * 30, 
                self.canvas_width - 180, 
                self.margin + i * 30 + 20, 
                fill=colors[i % len(colors)],
                outline='black'
            )
            self.canvas.create_text(
                self.canvas_width - 170, 
                self.margin + i * 30 + 10, 
                text=junction, 
                anchor='w'
            )
    
    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        # Draw histogram and legend
        self.draw_histogram()
        self.add_legend()
        
        # Start Tkinter event loop
        self.root.mainloop()

def load_traffic_data(file_path):
    """
    Loads traffic data from a CSV file.
    
    :param file_path: Path to the CSV file
    :return: List of dictionaries containing traffic data
    """
    try:
        with open(file_path, 'r') as csvfile:
            # Use csv.DictReader to automatically use first row as headers
            reader = csv.DictReader(csvfile)
            
            # Convert to list to allow multiple iterations
            traffic_data = list(reader)
        
        if not traffic_data:
            print(f"Warning: No data found in {file_path}")
        
        return traffic_data
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except csv.Error as e:
        print(f"CSV Error: {e}")
        return []

# Example usage in main script
file_path = 'traffic_data15062024.csv'
data = load_traffic_data(file_path)
app = HistogramApp(data, '2024-06-15')
app.run()