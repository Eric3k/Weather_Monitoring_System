import requests
import json
import logging
import schedule
import time
import os
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenWeatherMap API configuration
OPENWEATHERMAP_API_KEY = '1f6195682689ea412d3d809dec331bf9'
OPENWEATHERMAP_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
CITY_NAMES = ['Mumbai', 'New York', 'London', 'Tokyo', 'Sydney']

# Splunk HEC configuration
SPLUNK_HEC_URL = os.environ.get('SPLUNK_HEC_URL')  # Get from environment variable
SPLUNK_HEC_TOKEN = os.environ.get('SPLUNK_HEC_TOKEN') # Get from environment variable

def fetch_weather_data():
    """Fetch weather data from OpenWeatherMap API."""
    try:
        weather_data_list = []
        for CITY_NAME in CITY_NAMES:
            params = {'q': CITY_NAME, 'appid': OPENWEATHERMAP_API_KEY, 'units': 'metric'}
            response = requests.get(OPENWEATHERMAP_API_URL, params=params)
            response.raise_for_status()
            logging.info(f"Weather data fetched successfully for {CITY_NAME}.")
            weather_data_list.append(response.json())
        return weather_data_list
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

def format_data_for_splunk(weather_data):
    """Format weather data for Splunk HEC."""
    try:
        logging.debug(f"Raw weather data received for formatting: {weather_data}")
        formatted_data = {
            "event": "weather_data",
            "fields": {
                "city": weather_data.get("name"),
                "temperature": weather_data["main"].get("temp"),
                "humidity": weather_data["main"].get("humidity"),
                "weather": weather_data["weather"][0].get("description"),
                "timestamp": weather_data.get("dt")
            }
        }
        logging.info("Weather data formatted for Splunk.")
        return formatted_data
    except KeyError as e:
        logging.error(f"Error formatting data for Splunk: {e}")
        return None

def send_to_splunk(data):
    """Send formatted data to Splunk HEC."""
    try:
        logging.debug(f"Preparing to send data to Splunk: {data}")
        headers = {
            'Authorization': f'Splunk {SPLUNK_HEC_TOKEN}',
            'Content-Type': 'application/json'
        }
        logging.debug(f"Using headers: {headers}")
        response = requests.post(SPLUNK_HEC_URL, headers=headers, data=json.dumps(data))
        logging.debug(f"Splunk response status code: {response.status_code}")
        response.raise_for_status()
        logging.info("Data sent to Splunk successfully.")
        time.sleep(120)  # Sleep for 2 minutes
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to Splunk: {e}")
        logging.debug(f"Failed data payload: {data}")
    weather_data_list = fetch_weather_data()
    for weather_data in weather_data_list:
        if weather_data:
            formatted_data = format_data_for_splunk(weather_data)
            if formatted_data:
                send_to_splunk(formatted_data)
        formatted_data = format_data_for_splunk(weather_data)
        if formatted_data:
            send_to_splunk(formatted_data)

# Schedule the job to run every 5 minutes
def job():
    """Job to fetch weather data and send to Splunk."""
    weather_data_list = fetch_weather_data()
    if weather_data_list:
        for weather_data in weather_data_list:
            if weather_data:
                formatted_data = format_data_for_splunk(weather_data)
                if formatted_data:
                    send_to_splunk(formatted_data)

schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    logging.info("Weather monitoring system started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
