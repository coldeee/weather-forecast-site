import json

def check_bad_weather():
    try:
        with open("weather_data.json", "r", encoding='utf-8') as file:
            weather_data = json.load(file)
            #Считаем по дефолту что погода хорошая
            conditions = True 

            #Считаем плохую погоду если температура ниже -10 или выше 35,
            #если скорость ветра больше 35, или если вероятность дождя больше 85    
            for city in weather_data:
                if city['temperature'] < -10 or city['temperature'] > 35:
                    conditions = False
                elif city['wind_speed'] > 35:
                    conditions = False
                elif city['rain_prob'] > 70:
                    conditions = False
            
            #Проверяем условия, без уточнения в какои именно из городов плохая погода
            if not conditions:
                return f"Ой-ой, погода в одном из городов плохая"
            else:
                return "Погода в обоих городах — супер"
  
    except Exception as e:
        print(f"Ошибка при проверке погоды: {e}")
        return "Ошибка при проверке погоды"