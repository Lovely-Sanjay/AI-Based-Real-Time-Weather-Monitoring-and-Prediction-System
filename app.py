from flask import Flask, render_template, request
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ Create history table if not exists
def create_history_table():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        temperature REAL,
                        humidity REAL,
                        wind REAL,
                        time TEXT)''')
    conn.commit()
    conn.close()

# ✅ Save data into history
def save_history(city, temperature, humidity, wind):
    create_history_table()  # ensure table exists
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (city, temperature, humidity, wind, time) VALUES (?, ?, ?, ?, ?)",
                   (city, temperature, humidity, wind, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# ✅ Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    forecast_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city'].strip()

        if not city:
            error = "⚠ Please enter a city name!"
            return render_template('index.html', weather_data=None, forecast_data=None, error=error)

        api_key = "68d17341187d5a01cb7046c139958887"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        weather_response = requests.get(url).json()

        if weather_response.get('cod') != 200:
            error = "❌ Invalid city name! Please try again."
        else:
            weather_data = weather_response
            forecast_data = requests.get(forecast_url).json()

            # ✅ Save only valid data to history
            save_history(city, weather_data['main']['temp'], weather_data['main']['humidity'], weather_data['wind']['speed'])

    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, error=error)

# ✅ History Route
@app.route('/history')
def history():
    create_history_table()  # ensure table exists
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT city, temperature, humidity, wind, time FROM history ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('history.html', records=records)

if __name__ == "__main__":
    app.run(debug=True)
