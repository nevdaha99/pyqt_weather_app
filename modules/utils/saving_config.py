import json
import os

config_path = os.path.abspath(__file__ + "/../../../config.json")


def get_config():
    with open(config_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
        return data


def save_config(list_city, selected_city, is_dark):
    data = {
        "list_city": list_city,
        "selected_city": selected_city,
        "is_dark": is_dark,
    }
    with open(config_path, "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
