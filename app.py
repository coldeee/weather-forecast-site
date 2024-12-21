from flask import Flask, render_template, request
import re
import json
import requests

from utils.get_info import get_location, get_weather_by_location
from utils.weather_checker import check_bad_weather
from utils.file_reader import save_both_to_json
from utils.visualize import create_dash_app

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        start_location = request.form.get('start_location')
        end_location = request.form.get('end_location')
        forecast_days = int(request.form.get('forecast_days', 1))

        # Проверка формата ввода
        pattern = re.compile('^[А-Яа-яЁёA-Za-z\s]+$')

        if not pattern.match(start_location) or not pattern.match(end_location):
            error_message = "Некорректный формат ввода. Пожалуйста, используйте только буквы."
            return render_template('index.html', error=error_message)

        # Получение ключей местоположений
        start_key = get_location(start_location)
        end_key = get_location(end_location)

        if not start_key:
            error_message = f"Не удалось найти местоположение {start_location}"
            return render_template('index.html', error=error_message)
        elif not end_key:
            error_message = f"Не удалось найти местоположение {end_location}"
            return render_template('index.html', error=error_message)   

        # Получение погодных данных
        start_weather = get_weather_by_location(start_key[0], start_location)
        end_weather = get_weather_by_location(end_key[0], end_location)

        if not start_weather or not end_weather:
            error_message = "Не удалось получить данные о погоде."
            return render_template('index.html', error=error_message)

        # Сохранение данных и оценка погоды
        save_both_to_json(start_weather, end_weather)
        weather_evaluation = check_bad_weather()
        
        if isinstance(weather_evaluation, list):
            weather_evaluation = [
                [day for day in city if day['day'] <= forecast_days]
                for city in weather_evaluation
            ]
        
        return render_template('result.html',
                            evaluation=weather_evaluation,
                            start=start_key[1],
                            end=end_key[1],
                            start_weather=start_weather[:forecast_days],
                            end_weather=end_weather[:forecast_days],
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












