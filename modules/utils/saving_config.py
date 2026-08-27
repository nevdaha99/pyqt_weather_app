import json
import os

config_path = os.path.abspath(__file__ + "/../../../config.json")


def get_default_config():
    return {
        "list_city": [],
        "selected_city": "",
        "is_dark": True,
        "size": "1200x800",
        "image_pack": "pack1",
        "language": "ua",
        "settings_language": {
            "ua": {
                "title": "Налаштування",
                "search_city_button": "Пошук міста",
                "app_size_button": "Розмір додатку",
                "language_button": "Мова додатку",
                "image_list_button": "Списки зображень",
                "coordinat_title": "Координати",
                "coordinat_input": "наприклад: 50.4501, 30.5234",
                "save_button": "Зберегти",
                "added_city_label": "Додані міста",
                "size_title": "Оберіть розмір додатку",
                "language_title": "Оберіть мову додатку",
                "list1_title": "Список зображень №1",
                "list2_title": "Список зображень №2",
            },
            "en": {
                "title": "Settings",
                "search_city_button": "Search City",
                "app_size_button": "App Size",
                "language_button": "App Language",
                "image_list_button": "Image Lists",
                "coordinat_title": "Coordinates",
                "coordinat_input": "e.g.: 50.4501, 30.5234",
                "save_button": "Save",
                "added_city_label": "Added Cities",
                "size_title": "Choose App Size",
                "language_title": "Choose App Language",
                "list1_title": "Image List #1",
                "list2_title": "Image List #2",
            },
        },
    }


def get_config():
    if not os.path.exists(config_path):
        data = get_default_config()
        with open(config_path, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return data

    with open(config_path, "r", encoding="UTF-8") as file:
        return json.load(file)


def save_config(list_city, selected_city, is_dark, size, image_pack, lang):
    data = get_default_config()

    data["list_city"] = list_city
    data["selected_city"] = selected_city
    data["is_dark"] = is_dark
    data["size"] = size
    data["image_pack"] = image_pack
    data["language"] = lang

    with open(config_path, "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
