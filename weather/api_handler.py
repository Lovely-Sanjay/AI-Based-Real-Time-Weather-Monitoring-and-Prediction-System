import requests
import os

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def fetch_weather(self, city):
        """Fetch current weather data for a given city with error handling"""
        if not city:
            return {"error": "City name cannot be empty."}

        if not self.api_key:
            return {"error": "Missing or invalid API key."}

        try:
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            res = requests.get(self.weather_url, params=params, timeout=8)
            data = res.json()

            if res.status_code != 200:
                return {"error": data.get("message", "Unknown error")}

            # ✅ Add icon-type to make frontend easier
            condition = data["weather"][0]["description"].lower()
            icon = self.get_icon(condition)

            data["icon"] = icon
            return data

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def fetch_forecast(self, city):
        """Fetch 5-day forecast (1 record per day) with added icon field"""
        if not city:
            return {"error": "City name cannot be empty."}

        try:
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            res = requests.get(self.forecast_url, params=params, timeout=8)
            data = res.json()

            if res.status_code != 200:
                return {"error": data.get("message", "Unknown error")}

            daily_forecast = []
            for i in range(0, len(data["list"]), 8):
                day = data["list"][i]
                condition = day["weather"][0]["description"].lower()

                daily_forecast.append({
                    "date": day["dt_txt"].split(" ")[0],
                    "temp": day["main"]["temp"],
                    "condition": condition,
                    "icon": self.get_icon(condition)  # ✅ Icon added
                })

            return daily_forecast

        except Exception as e:
            return {"error": f"Unexpected forecast error: {str(e)}"}

    def get_icon(self, condition):
        """Map condition text to icon name"""
        if "rain" in condition:
            return "rain"
        elif "cloud" in condition:
            return "cloud"
        elif "sun" in condition or "clear" in condition:
            return "sun"
        else:
            return "cloud"
