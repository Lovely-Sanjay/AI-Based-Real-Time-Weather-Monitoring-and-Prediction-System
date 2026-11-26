import csv
import os
from datetime import datetime

class WeatherLogger:
    def __init__(self, filename="weather_history.csv"):
        self.filename = filename
        # Create CSV file with headers if not exists
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["City", "Temperature (°C)", "Humidity (%)", "Condition", "Timestamp"])

    def log(self, data):
        try:
            city = data.get("name", "Unknown")
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(self.filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([city, temp, humidity, condition, timestamp])
        except Exception as e:
            print(f"Error logging: {e}")

    def read_logs(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)
