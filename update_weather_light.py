def update_weather_light(light_id):
    # Get the list of colors and the current color index from variables
    colors = hass.states.get("var.weather_colors").state
    color_index = hass.states.get("var.weather_color_index").state
    
    logger.info(colors)
    
    if colors is not None and color_index is not None:
        # Split the colors string into a list
        color_list = colors.split(";")
        
        color_index_int = int(color_index)
        
        # If the index is beyond the scope of the list, reset it to 0
        if int(color_index_int) >= len(color_list) or color_index_int < 0:
            color_index_int = 0
        
        logger.info(color_index_int)
        
        # Get the RGB colors from the color string
        color_rgb = [int(x) for x in color_list[color_index_int].split(",")]
        
        # Set the bulb color
        set_bulb_color(light_id, color_rgb)
        logger.info(color_rgb)
        
        # Increment the color index variable
        hass.states.set("var.weather_color_index", color_index_int + 1)

def set_bulb_color(light_id, color):
    # Set the color of the specified light bulb
    service_data = {"entity_id": light_id, "rgb_color": color, "brightness": 255}
    hass.services.call("light", "turn_on", service_data, False)

# Get the entity ID for the bulb we want to use for the weather light
entity_id = data.get("entity_id")

if entity_id is not None:
    update_weather_light(entity_id)
