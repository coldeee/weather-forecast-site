from flask import Flask, render_template, request
import re

from utils.get_info import get_location, get_weather_by_location
from utils.weather_checker import check_bad_weather
from utils.file_reader import save_both_to_json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        start_location = request.form.get('start_location')
        end_location = request.form.get('end_location')

        # Проверка формата ввода: только буквы и пробелы (например, "Нью Йорк")

        pattern = re.compile(r'^[А-Яа-яЁёA-Za-z\s]+$')

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

        # Получение погодных данных для обоих местоположений
        start_weather = get_weather_by_location(start_key[0])
        end_weather = get_weather_by_location(end_key[0])

        if not start_weather or not end_weather:
            # Если не удалось получить данные о погоде, отображаем ошибку
            error_message = "Не удалось получить данные о погоде."
            return render_template('index.html', error=error_message)

        # Сохранение погодных данных в JSON-файл
        save_both_to_json(start_weather, end_weather)

        # Оценка погодных условий
        evaluation = check_bad_weather()

        # Отображение результатов на странице
        return render_template('result.html', evaluation=evaluation, 
                               start=start_key[1], end=end_key[1],
                               start_weather=start_weather, end_weather=end_weather)
    
    # Если метод GET, отображаем главную страницу
    return render_template('index.html')

if __name__ == '__main__':
    #Запуск приложения в режиме отладки (для удобства)
    app.run(debug=True)










