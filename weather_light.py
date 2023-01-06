import requests
import json

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

def get_weather_data(latitude, longitude):
    # API key and base URL
    API_KEY = "YOUR_API_KEY"
    base_url = "https://api.openweathermap.org/data/2.5/"

    # Query current weather and forecast for the next 8 hours
    query_url = base_url + "onecall?lat=" + latitude + "&lon=" + longitude + "&exclude=daily,minutely&units=imperial&appid=" + API_KEY

    # Make API call and store the response
    response = requests.get(query_url)

    # Convert the response to JSON
    data = response.json()

    return data

def get_bulb_color(weather_data):
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

    # Loop through each hour of forecast data
    for hour in weather_data['hourly'][:8]:
        # Get the weather id
        weather_id = hour['weather'][0]['id']

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
        if hour['temp'] <= 32 or hour['feels_like'] <= 32:
            is_cold = True
        if hour['temp'] >= 80 or hour['feels_like'] >= 80:
            is_hot = True

        # Check if it's cloudy, windy, or humid
        if hour['clouds'] > 50 and not will_rain and not will_snow and not will_sleet:
            is_cloudy = True
        if hour['dew_point'] >= 65:
            is_humid = True
        if hour['wind_speed'] >= 25 or hour['wind_gust'] >= 30:
            is_windy = True

    # Check if there are any alerts
    if 'alerts' in weather_data:
        is_alert = True

    # If none of the above conditions are met, it's clear
    if not (will_    rain or will_snow or will_sleet or is_cold or is_hot or is_cloudy or is_windy or is_humid or is_alert):
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

def update_bulb_color(latitude, longitude):
    weather_data = get_weather_data(latitude, longitude)
    colors = get_bulb_color(weather_data)

    # Change the bulb color every 5 seconds if there is more than one color
    while len(colors) > 1:
        for color in colors:
            # Set the bulb color to the current color
            set_bulb_color(color)
            # Wait for 5 seconds
            time.sleep(5)
        # After looping through all the colors once, get the updated weather data and colors
        weather_data = get_weather_data(latitude, longitude)
        colors = get_bulb_color(weather_data)

    # If there is only one color, set the bulb to that color
    elif len(colors) == 1:
        set_bulb_color(colors[0])

# Query the weather data and update the bulb color every 60 seconds
while True:
    update_bulb_color(latitude, longitude)
    time.sleep(60)
