import json
import folium
from folium import plugins
from utils.get_info import get_location, geo_position

def create_weather_map_from_json(location_keys=None, weather_data=None):
    #Создание карты с данными погоды
    
    # Если параметры не переданы, пытаемся загрузить из файла
    if location_keys is None or weather_data is None:
        try:
            with open('weather_data.json', 'r', encoding='utf-8') as file:
                weather_data = json.load(file)
                
                # Получаем список городов из первых записей
                cities = []
                coordinates = []
                
                for city_data in weather_data:
                    if city_data and len(city_data) > 0:
                        city_name = city_data[0]['location']
                        cities.append(city_name)
                        # Получаем ключ локации для города
                        location_data = get_location(city_name)
                        if location_data:
                            location_key = location_data[0]
                            # Получаем координаты
                            coords = geo_position(location_key)
                            if coords:
                                coordinates.append([coords['lat'], coords['lon']])
                                print(f"Добавлены координаты для {city_name}: {coordinates[-1]}")
                
                if not coordinates:
                    print("Не удалось получить координаты")
                    return None
                
                # Создаем карту
                print("Создание карты...")
                m = folium.Map(location=coordinates[0], zoom_start=4)
                
                # Добавляем маркеры
                for i, (coord, city_data) in enumerate(zip(coordinates, weather_data)):
                    weather_info = f"<b>{cities[i]}</b><br><br>"
                    for day in city_data:
                        weather_info += (
                            f"<b>День {day['day']}:</b><br>"
                            f"Температура: {day['temperature']}°C<br>"
                            f"Влажность: {day['humidity']}%<br>"
                            f"Ветер: {day['wind_speed']} км/ч<br>"
                            f"Вероятность осадков: {day['rain_prob']}%<br><br>"
                        )
                    
                    folium.Marker(
                        coord,
                        popup=folium.Popup(weather_info, max_width=300),
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                
                # Добавляем маршрут
                if len(coordinates) > 1:
                    folium.PolyLine(
                        coordinates,
                        weight=2,
                        color='blue',
                        opacity=0.8
                    ).add_to(m)
                
                plugins.Fullscreen().add_to(m)
                print("Карта создана успешно")
                
                return m
                
        except Exception as e:
            print(f"Ошибка при создании карты: {e}")
            return None

def create_default_map():
    #Создание пустой карты с центром в России
    m = folium.Map(
        location=[55.7558, 37.6173],  # Координаты центра России (Москва)
        zoom_start=4
    )
    
    # Добавляем элементы управления
    plugins.Fullscreen().add_to(m)
    
    return m 