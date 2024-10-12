import requests
from flask import Blueprint, jsonify, request

weather_bp = Blueprint('weather', __name__)
OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'

API_KEY = 'ec5d40120c4b1a065a30c61a13780d09'
AQI_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'
GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'

def get_city_coordinates(city):
    """Fetch the latitude and longitude of a city using OpenWeather Geocoding API."""
    params = {
        'q': city,
        'limit': 1,
        'appid': API_KEY
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()

    if len(data) > 0:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

# Current weather endpoint
@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Berlin')  # Default to Berlin
    lat, lon = get_city_coordinates(city)

    if lat is None or lon is None:
        return jsonify({"error": "City not found"}), 404

    print(f"Coordinates for {city}: lat={lat}, lon={lon}")  # Debug log

    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': True,
        'timezone': 'auto',  # Optional: to get the timezone of the location
        'alerts': True  # Request alerts
    }
    
    response = requests.get(OPEN_METEO_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': city,
            'current': {
                'temperature': f"{data['current_weather']['temperature']}°C",
                'description': data['current_weather'].get('weathercode', 'No description'),  # Handle missing descriptions
                'wind_speed': data['current_weather'].get('windspeed', 'No wind speed data'),  # Safely access wind speed
                'humidity': data['current_weather'].get('humidity', 'No humidity data'),  # Safely access humidity
            },
            'alerts': data.get('alerts', [])  # Extract alerts from the response
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "Unable to fetch weather data"}), response.status_code

# Air Quality endpoint
@weather_bp.route('/air_quality', methods=['GET'])
def get_air_quality():
    city = request.args.get('city', 'Berlin')  # Default to Berlin
    lat, lon = get_city_coordinates(city)

    if lat is None or lon is None:
        return jsonify({"error": "City not found"}), 404

    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY
    }
    
    response = requests.get(AQI_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        aqi_info = {
            'city': city,
            'aqi': data['list'][0]['main']['aqi'],
            'components': data['list'][0]['components']
        }
        return jsonify(aqi_info)
    else:
        return jsonify({"error": "Unable to fetch air quality data"}), response.status_code