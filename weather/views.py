from flask import Blueprint, render_template, request
from weather.api_handler import WeatherAPI
from weather.logger import WeatherLogger
from weather.models import WeatherLog   # ✅ Import database model

weather_bp = Blueprint('weather', __name__)
api = WeatherAPI()
logger = WeatherLogger()

# ----------------------- HOME PAGE -----------------------
@weather_bp.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city', '').strip()

        # ✅ Allow letters, spaces, dash and apostrophes (No strict rejection like before)
        # ❌ Removed old regex that rejected names like Vizag, Vizianagaram, New Delhi, O'Connor
        if not city:
            error = "City name cannot be empty."
        else:
            weather_data = api.fetch_weather(city)

            if 'error' in weather_data:
                error = weather_data['error']
            else:
                forecast_data = api.fetch_forecast(city)

                if isinstance(forecast_data, dict) and 'error' in forecast_data:
                    error = forecast_data['error']
                else:
                    # ✅ Save weather to DB or CSV log
                    logger.log(weather_data)

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, error=error)


# ----------------------- HISTORY PAGE -----------------------
@weather_bp.route('/history')
def history():
    # ✅ Fetch weather logs from the database
    logs = WeatherLog.query.order_by(WeatherLog.timestamp.desc()).all()

    # ✅ OPTIONAL: Fetch forecast for each city stored in DB
    city_forecasts = {}
    cities = {log.city for log in logs} if logs else set()

    for city in cities:
        forecast = api.fetch_forecast(city)
        if isinstance(forecast, list):  # ✅ Only add valid forecast
            city_forecasts[city] = forecast

    return render_template('history.html', logs=logs, city_forecasts=city_forecasts)
