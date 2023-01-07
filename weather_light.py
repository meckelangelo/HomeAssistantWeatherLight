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

# Get the entity ID for the bulb we want to use for the weather light
entity_id = data.get("entity_id")

if entity_id is not None:
    while True:
        update_weather_light(entity_id)

def get_condition_colors(weather_sensor):
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
    has_alert = False

    # Initialize an empty list of colors
    colors = []
    
    # Create the list to store the weather conditions
    weather_conditions = []

    # Get the current and forecast weather data
    current_weather = weather_sensor.attributes.get("current")
    forecast_data = weather_sensor.attributes.get("forecast")[:8]
    if current_weather and forecast_data:
        # Combine the current and forecast weather conditions into a single list
        weather_conditions = current_weather.get("weather") + [forecast_weather for forecast in forecast_data for forecast_weather in forecast.get("weather")]
        # Check if there are any alerts in the current or forecast weather data
        has_alert = any(data.get("alert") for data in ([current_weather] + forecast_data))
    
    # Loop through each condition
    for condition in weather_conditions

        # Get the weather condition ID
        weather_id = condition.get("id")
    
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
        temperature = condition.get("temperature")
        feels_like = condition.get("feels_like")
        if temperature <= 32 or feels_like <= 32:
            is_cold = True
        if temperature >= 80 or feels_like >= 80:
            is_hot = True

        # Check if it's cloudy, windy, or humid
        if condition.get("clouds") > 50 and not will_rain and not will_snow and not will_sleet:
            is_cloudy = True
        if condition.get("dew_point") >= 65:
            is_humid = True
        if condition.get("wind_speed") >= 25 or condition.get("wind_gust") >= 30:
            is_windy = True

    # If none of the above conditions are met, it's clear
    if not (will_rain or will_snow or will_sleet or is_cold or is_hot or is_cloudy or is_windy or is_humid or has_alert):
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
    if has_alert:
        colors.append(RED)

    return colors

def update_weather_light(light_id):
    weather_data = hass.states.get("weather.openweathermap_overview")
    colors = get_condition_colors(weather_data)

    # Change the bulb color every 5 seconds
    for color in colors:
        # Set the bulb color to the current color
        set_bulb_color(light_id, color)
        # Wait for 5 seconds
        time.sleep(5)

def set_bulb_color(light_id, color):
    hue, saturation = color
    # Set the hue and saturation of the specified light bulb
    service.call("light", "turn_on", {"entity_id": light_id, "hue": hue, "saturation": saturation})
