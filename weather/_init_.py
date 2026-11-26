from flask import Flask

def create_app():
    app = Flask(__name__)

    from weather.views import weather_bp
    app.register_blueprint(weather_bp)

    return app
