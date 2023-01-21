# Color constants
BLUE = [20, 20, 100]
AQUA = [0, 150, 255]
TEAL = [0, 225, 180]
GREEN = [0, 25, 0]
LIME = [165, 255, 0]
YELLOW = [255, 255, 0]
ORANGE = [255, 125, 0]
RED = [150, 5, 15]
PURPLE = [145, 0, 225]
MAGENTA = [255, 0, 255]

def get_condition_colors(weather_sensor):
    # Initialize all the booleans to false
    will_rain = False
    will_snow = False
    will_lightning = False
    is_cold = False
    is_hot = False
    is_cloudy = False
    is_windy = False
    is_humid = False
    is_clear = False
    is_hazardous = False

    # Initialize an empty list of colors
    colors = []

    # Create the list to store the weather conditions
    weather_conditions = []
    temperatures = []
    dew_points = []
    wind_speeds = []
    

    # Get the current and forecast weather conditions
    weather_conditions.append(weather_sensor.state)
    
    # Get the temperature and relative humidity, and use them to estimate the dew point
    temperature = weather_sensor.attributes.get("temperature")
    humidity = weather_sensor.attributes.get("humidity")
    dew_point = 0
    if humidity is not None:
        dew_point = temperature - ((100 - humidity) * (9 / 25))
    logger.info(dew_point)
    
    # Add the temperature and dew point to their lists
    temperatures.append(temperature)
    dew_points.append(dew_point)
    
    # Get the current wind speed
    wind_speeds.append(weather_sensor.attributes.get("wind_speed"))
    
    # Get the next 8 hours of forecast and get the same information for each hour
    if weather_sensor.attributes.get("forecast") is not None:
        forecasts = weather_sensor.attributes.get("forecast")[:8]
        for forecast in forecasts:
            weather_conditions.append(forecast["condition"])
            
            temperature = forecast["temperature"]
            #humidity = forecast["humidity"]
            #dew_point = ((temperature - ((100 - humidity) / 5)) * 1.8) + 32
            
            temperatures.append(temperature)
            #dew_points.append(dew_point)
            
            wind_speeds.append(forecast["wind_speed"])

    # Loop through each condition
    for condition in weather_conditions:
        if condition in ("rainy", "lightning", "lightning-rainy", "pouring", "snowy-rainy"):
            will_rain = True
            logger.info("Rain")
        if condition in ("snowy", "snowy-rainy"):
            will_snow = True
            logger.info("Snow")
        if condition in ("lightning, lightning-rainy"):
            will_lightning = True
            logger.info("Lightning")
        if condition in ("fog", "hail", "exceptional"):
            is_hazardous = True
            logger.info("Hazardous")
        if condition in ("cloudy", "partlycloudy"):
            is_cloudy = True
            logger.info("Cloudy")
    
    # Loop through each temperature and record whether it will be excessively cold or hot
    for temperature in temperatures:
        if temperature <= 32:
            is_cold = True
            logger.info("Cold")
        if temperature >= 80:
            is_hot = True
            logger.info("Hot")
    
    # Loop through each dew point and record whether it will be excessively humid
    for dew_point in dew_points:
        if dew_point >= 65:
            is_humid = True
            logger.info("Humid")
    
    # Loop through each wind speed and record whether it will be excessively windy
    for wind_speed in wind_speeds:
        if wind_speed >= 25:
            is_windy = True
            logger.info("Windy")
    
    # If it's not going to be rainy, snowy, cloudy, etc. then it will be clear
    if not (will_rain or will_snow or will_lightning or is_hazardous or is_cloudy):
        is_clear = True
        logger.info("Clear")

    # Determine the colors based on the active booleans
    if will_rain:
        colors.append(AQUA)
    if will_snow:
        colors.append(PURPLE)
    if will_lightning:
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
    if is_hazardous:
        colors.append(RED)

    return colors

def get_test_colors():
    colors = []
    colors.append(BLUE)
    colors.append(AQUA)
    colors.append(TEAL)
    colors.append(GREEN)
    colors.append(LIME)
    colors.append(YELLOW)
    colors.append(ORANGE)
    colors.append(RED)
    colors.append(MAGENTA)
    colors.append(PURPLE)
    
    return colors

def update_weather_light(light_id):
    weather_sensor = hass.states.get("weather.openweathermap_overview")
    colors = get_condition_colors(weather_sensor)
    #colors = get_test_colors()

    # Change the bulb color every 5 seconds
    for color in colors:
        # Set the bulb color to the current color
        set_bulb_color(light_id, color)
        logger.info(color)
        # Wait for 5 seconds
        time.sleep(5)

def set_bulb_color(light_id, color):
    # Set the color of the specified light bulb
    service_data = {"entity_id": light_id, "rgb_color": color, "brightness": 255}
    hass.services.call("light", "turn_on", service_data, False)

# Get the entity ID for the bulb we want to use for the weather light
entity_id = data.get("entity_id")

if entity_id is not None:
    while True:
        update_weather_light(entity_id)
