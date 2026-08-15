from .get_weather import get_weather


def get_graphic(city_name):
    data = get_weather(city_name, True)
    temp_list = []
    height_list = []
    for weather in data["list"]:
        temp = weather["main"]["temp"]
        temp_list.append(temp)
    min_temp = min(temp_list)
    min_visible_temp = round(min_temp / 5) * 5 - 10
    for temp in temp_list:
        height = round((temp - min_visible_temp) * 2.874)
        height_list.append(height)
    return min_visible_temp, height_list
