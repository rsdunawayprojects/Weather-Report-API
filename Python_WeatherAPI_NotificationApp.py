import requests
from win11toast import toast
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file_path = os.path.join(os.getcwd(), 'weatherlog.txt')
file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# User-Agent header to avoid blocking by the website
headers = {
    'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

# Geo coordinates for weather location and authentication api key with url format for scraping 
lat = 41.6639
lon = -83.5552
API_key = ""
url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_key}"

# Converting kelvin reading into Celsius and Fahrenheit for user
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

# The format to scrape and retrieve api data
def get_weather(data):
    weather_description = data['current']['weather'][0]['description']
    wind_speed = data['current']['wind_speed']
    humidity = data['current']['humidity']
    current_temp_k = data['current']['temp']
    current_temp_c, current_temp_f = kelvin_to_celsius_fahrenheit(current_temp_k)
    current_feels_like_k = data['current']['feels_like']
    current_feels_like_c, current_feels_like_f = kelvin_to_celsius_fahrenheit(current_feels_like_k)
    
    
    
    return weather_description, current_temp_c, current_temp_f, wind_speed, humidity, current_feels_like_c, current_feels_like_f 

# Function to display toast notification 
def display_notification(weather_info):
    weather_description, current_temp_c, current_temp_f, wind_speed, humidity, current_feels_like_c, current_feels_like_f = weather_info
    message = (f"Weather Description: {weather_description}\n"
               f"Current Winds: {wind_speed:.2f}mph\n"
               f"Humidity: {humidity}%\n"
               f"Current Temperature: {current_temp_f:.2f}°F\n"
               f"Feels Like: {current_feels_like_f:.2f}°F\n")
    toast("Weather Report 🌤", message, button='Dismiss')
    # {'arguments': 'http:', 'user_input': {}}
    return"Thanks For Using Your Favorite Python API For Weather!"

 
# Log the scraped weather information displayed to the user to a file for viewing
def log_weather_info(weather_info):
    weather_description, current_temp_c, current_temp_f, wind_speed, humidity, current_feels_like_c, current_feels_like_f = weather_info
    log_message = (f"\nWeather Description: {weather_description}\n"
                   f"Current Winds: {wind_speed:.2f}mph\n"
                   f"Humidity: {humidity}%\n"
                   f"Current Temperature: {current_temp_f:.2f}°F\n"
                   f"Feels Like: {current_feels_like_f:.2f}°F\n")
                   
    
# Log scraped data to logger
    logger.info(log_message)


# Performs the primary function making the call to display toast notification and log
def main():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = get_weather(data)
        toast(display_notification(weather_info))
        log_weather_info(weather_info)  
    else:
        logger.error(f"Failed to retrieve weather data: {response.status_code}")

if __name__ == "__main__":
    main()

