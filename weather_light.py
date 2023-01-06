from datetime import datetime
import requests
import json
import homeassistant.helpers.service as service

# Color constants
BLUE = [68, 100]
AQUA = [56, 100]
TEAL = [45, 100]
GREEN = [36, 100]
LIME = [22, 100]
YELLOW = [14, 100]
ORANGE = [10, 100]
RED = [0, 100]
PURPLE = [78, 100]
MAGENTA = [88, 100]

def get_weather_data():
    # API key and base URL
    API_KEY = "YOUR_API_KEY"
    latitude = 40.20013016138404
    longitude = -76.63915972486825

    # Query current weather and forecast for the next 8 hours
    query_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + latitude + "&lon=" + longitude + "&exclude=daily,minutely&units=imperial&appid=" + API_KEY

    # Make API call and store the response
    response = requests.get(query_url)

    # Convert the response to JSON
    return response.json()

def get_condition_colors(weather_data):
    # Initialize all the booleans to false
    will_rain = False
    will_snow = False
    will_sleet = False
    is_cold = False
    is_hot = False
    is_cloudy = False
    is_windy = False
    is_humid = False
    is_clear = False
    is_alert = False

    # Initialize an empty list of colors
    colors = []
    
    # Initialize an empty list of conditions
    conditions_set = []
    
    # Add the current conditions to the list
    conditions_set.append(weather_data['current'])
    
    # Loop through the first 8 hours of forecast data and add it to the conditions
    for hour in weather_data['hourly'][:8]:
        conditions_set.append(hour)
    
    # Loop through each condition
    for conditions in conditions_set
        # Get the weather id
        weather_id = conditions['weather'][0]['id']

        # Check if it will rain or snow
        if 200 <= weather_id <= 599 or weather_id == 701:
            will_rain = True
        if weather_id in (600, 601):
            will_snow = True
        if weather_id in (611, 612, 613):
            will_sleet = True
        if 615 <= weather_id <= 621:
            will_rain = will_snow = True

        # Check if it's cold or hot
        if conditions['temp'] <= 32 or conditions['feels_like'] <= 32:
            is_cold = True
        if conditions['temp'] >= 80 or conditions['feels_like'] >= 80:
            is_hot = True

        # Check if it's cloudy, windy, or humid
        if conditions['clouds'] > 50 and not will_rain and not will_snow and not will_sleet:
            is_cloudy = True
        if conditions['dew_point'] >= 65:
            is_humid = True
        if conditions['wind_speed'] >= 25 or conditions['wind_gust'] >= 30:
            is_windy = True

    # Check if there are any alerts
    if 'alerts' in weather_data:
        is_alert = True

    # If none of the above conditions are met, it's clear
    if not (will_rain or will_snow or will_sleet or is_cold or is_hot or is_cloudy or is_windy or is_humid or is_alert):
        is_clear = True

    # Determine the colors based on the active booleans
    if will_rain:
        colors.append(AQUA)
    if will_snow:
        colors.append(PURPLE)
    if will_sleet:
        colors.append(MAGENTA)
    if is_cold:
        colors.append(BLUE)
    if is_hot:
        colors.append(ORANGE)
    if is_cloudy:
        colors.append(TEAL)
    if is_windy:
        colors.append(YELLOW)
    if is_humid:
        colors.append(GREEN)
    if is_clear:
        colors.append(LIME)
    if is_alert:
        colors.append(RED)

    return colors

def update_weather_light(refresh_time):
    weather_data = get_weather_data()
    colors = get_condition_colors(weather_data)

    # Change the bulb color every 5 seconds
    while (datetime.now() < refresh_time):
        for color in colors:
                # Set the bulb color to the current color
                set_bulb_color(color)
                # Wait for 5 seconds
                time.sleep(5)

def set_bulb_color(color):
    hue, saturation = color
    # Replace YOUR_LIGHT_ENTITY_ID with the entity ID of your light bulb
    service.call("light", "turn_on", {"entity_id": YOUR_LIGHT_ENTITY_ID, "hue": hue, "saturation": saturation})

# Query the weather data and update the bulb color every 5 minutes
while True:
    refresh_seconds = 300
    refresh_time = datetime.now() + datetime.timedelta(seconds=refresh_seconds)
    
    update_weather_light(refresh_time)
