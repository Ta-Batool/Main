import requests
from flask import Blueprint, jsonify, request

weather_bp = Blueprint('weather', __name__)

API_KEY = 'ec5d40120c4b1a065a30c61a13780d09'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Berlin')  # Default to Berlin if no city is provided
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # To get temperature in Celsius
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract the relevant weather information
        weather_info = {
            'city': data['name'],
            'temperature': f"{data['main']['temp']}°C",
            'description': data['weather'][0]['description']
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "City not found"}), response.status_code
