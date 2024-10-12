from flask import Flask
from weather import weather_bp  # Import the blueprint from weather.py

app = Flask(__name__)

# Register blueprints for each functionality
app.register_blueprint(weather_bp)

@app.route('/')
def home():
    return "Welcome to the Weather API!<br>This gives you current weather data and air quality"

if __name__ == '__main__':
    app.run(debug=True)
