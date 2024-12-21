from flask import Flask, render_template, request
import re
import json
import requests

from utils.get_info import get_location, get_weather_by_location
from utils.weather_checker import check_bad_weather
from utils.visualize import create_dash_app
from utils.file_reader import save_to_json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение всех локаций из формы
        locations = request.form.getlist('locations[]')
        forecast_days = int(request.form.get('forecast_days', 1))

        # Проверка формата ввода для всех локаций
        pattern = re.compile('^[А-Яа-яЁёA-Za-z\s]+$')
        
        location_keys = []
        weather_data = []

        for location in locations:
            if not pattern.match(location):
                error_message = f"Некорректный формат ввода для {location}. Пожалуйста, используйте только буквы."
                return render_template('index.html', error=error_message)

            # Получение ключа местоположения
            location_key = get_location(location)
            if not location_key:
                error_message = f"Не удалось найти местоположение {location}"
                return render_template('index.html', error=error_message)

            # Получение погодных данных
            weather = get_weather_by_location(location_key[0], location)
            if not weather:
                error_message = f"Не удалось получить данные о погоде для {location}"
                return render_template('index.html', error=error_message)

            location_keys.append(location_key[1])
            weather_data.append(weather)

        # Сохранение данных
        save_to_json(weather_data)

        # Оценка погоды
        weather_evaluation = check_bad_weather()
        
        if isinstance(weather_evaluation, list):
            weather_evaluation = [
                [day for day in city if day['day'] <= forecast_days]
                for city in weather_evaluation
            ]
        
        return render_template('result.html',
                            evaluation=weather_evaluation,
                            locations=location_keys,
                            weather_data=weather_data,
                            forecast_days=forecast_days,
                            plot_url='/dash/')
    
    return render_template('index.html')

# Создаем экземпляр Dash приложения
dash_app = create_dash_app(app)

# Добавляем роут для Dash
@app.route('/dash/')
def dash_page():
    return dash_app.index()

if __name__ == '__main__':
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)  

    #Проверка валидности API ключа
    if settings['CHECK-API-KEY']:
        response = requests.get(
            "https://dataservice.accuweather.com"
            "/locations/v1/cities/translate.json",
            params={
                "apikey": settings['API_KEY'],
                "q": "london",
                "language": "ru-ru",
                "details": "true",
            },
        )
        if response.status_code != 200:
            print("API KEY не валиден")
            app = Flask(__name__)
            
            @app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
            @app.route('/<path:path>', methods=['GET', 'POST'])
            def api_error():
                return render_template('not_valid.html')
                
            app.run(debug=True)
        else:
            print("API KEY валиден")
            app.run(debug=True)
    else:
        print("Проверка API ключа отключена")
        app.run(debug=True)












