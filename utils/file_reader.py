import json

#Сохранение массива данных в json
def save_to_json(data):
    with open('weather_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#Используем для нашей формы из 2 городой (запись в json)
def save_both_to_json(start_weather, end_weather):
    weather = []
    weather.append(start_weather)
    weather.append(end_weather)
    save_to_json(weather, 'weather_data.json')  
