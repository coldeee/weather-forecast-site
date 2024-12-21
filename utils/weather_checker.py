import json

def check_bad_weather():
    try:
        with open("weather_data.json", "r", encoding='utf-8') as file:
            weather_data = json.load(file)
            results = []
            
            # Проходим по каждому городу
            for city_data in weather_data:
                city_results = []
                # Проходим по каждому дню
                for day in city_data:
                    conditions = True
                    reason = []
                    
                    # Проверяем условия погоды
                    if day['temperature'] < -10 or day['temperature'] > 35:
                        conditions = False
                        reason.append("экстремальная температура")
                    if day['wind_speed'] > 35:
                        conditions = False
                        reason.append("сильный ветер")
                    if day['rain_prob'] > 70:
                        conditions = False
                        reason.append("высокая вероятность осадков")
                    
                    # Формируем результат для каждого дня
                    status = {
                        'location': day['location'],
                        'day': day['day'],
                        'is_good': conditions,
                        'reason': ', '.join(reason) if reason else "погода хорошая",
                        'details': {
                            'temperature': f"{day['temperature']}°C",
                            'wind_speed': f"{day['wind_speed']} км/ч",
                            'rain_prob': f"{day['rain_prob']}%",
                            'humidity': f"{day['humidity']}%"
                        }
                    }
                    city_results.append(status)
                results.append(city_results)
            
            return results
            
    except Exception as e:
        print(f"Ошибка при проверке погоды: {e}")
        return "Ошибка при проверке погоды"