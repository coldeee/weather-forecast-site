from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import json

def create_dash_app(server):
    # Создаем экземпляр Dash с обновленными настройками
    dash_app = Dash(__name__, 
                    server=server, 
                    routes_pathname_prefix='/dash/',
                    external_stylesheets=['/static/css/main.css'],
                    external_scripts=['/static/js/background.js'],
                    index_string=open('templates/dash.html').read())
    
    # Функция для загрузки данных из JSON
    def load_weather_data():
        try:
            with open('weather_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return None

    # Создаем макет приложения
    dash_app.layout = html.Div([
        html.Div([
            html.Div([
                html.A('Назад', href='/', className='back-button', id='back-button'),
            ], className='header'),
            
            html.Div([
                dcc.Dropdown(
                    id='parameter-selector',
                    options=[
                        {'label': 'Температура', 'value': 'temperature'},
                        {'label': 'Влажность', 'value': 'humidity'},
                        {'label': 'Скорость ветра', 'value': 'wind_speed'},
                        {'label': 'Вероятность дождя', 'value': 'rain_prob'}
                    ],
                    value='temperature',
                    style={'width': '300px'}
                ),
                dcc.Dropdown(
                    id='days-selector',
                    options=[
                        {'label': '1 день', 'value': 1},
                        {'label': '3 дня', 'value': 3},
                        {'label': '5 дней', 'value': 5}
                    ],
                    value=1,
                    style={'width': '300px'}
                ),
            ], className='dropdown-container'),
            
            dcc.Graph(id='main-graph'),
        ], className='graphs-container')
    ], className='dash-container')

    # Настройки для графиков
    graphs_settings = {
        'temperature': {
            'title': 'Температура на маршруте',
            'yaxis_title': 'Температура (°C)',
            'color': 'rgb(239, 85, 59)'
        },
        'humidity': {
            'title': 'Влажность на маршруте',
            'yaxis_title': 'Влажность (%)',
            'color': 'rgb(99, 110, 250)'
        },
        'wind_speed': {
            'title': 'Скорость ветра на маршруте',
            'yaxis_title': 'Скорость ветра (км/ч)',
            'color': 'rgb(0, 204, 150)'
        },
        'rain_prob': {
            'title': 'Вероятность дождя на маршруте',
            'yaxis_title': 'Вероятность (%)',
            'color': 'rgb(171, 99, 250)'
        }
    }

    # Обновление основного графика при изменении параметра
    @dash_app.callback(
        Output('main-graph', 'figure'),
        [Input('parameter-selector', 'value'),
         Input('days-selector', 'value')]
    )
    def update_main_graph(selected_param, selected_days):
        data = load_weather_data()
        if not data:
            return create_empty_figure()

        settings = graphs_settings[selected_param]
        fig = go.Figure()

        # Для каждого города добавляем данные на график
        for city_data in data:
            if not city_data:  # Проверка на пустые данные
                continue
                
            location = city_data[0]['location']
            values = [day[selected_param] for day in city_data[:selected_days]]
            days = list(range(1, selected_days + 1))

            if selected_days == 1:
                # Столбчатая диаграмма для одного дня
                fig.add_trace(go.Bar(
                    x=[location],
                    y=[values[0]],
                    name=location,
                    marker_color=settings.get('color'),
                    width=0.4
                ))
            else:
                # Линейный график для нескольких дней
                fig.add_trace(go.Scatter(
                    x=days,
                    y=values,
                    mode='lines+markers',
                    name=location,
                    line=dict(width=3),
                    marker=dict(size=10)
                ))

        # Настройка макета в зависимости от количества дней
        if selected_days == 1:
            fig.update_layout(
                title=settings['title'],
                yaxis_title=settings['yaxis_title'],
                template='plotly_dark',
                height=500,
                margin=dict(t=50, b=50, l=50, r=50),
                plot_bgcolor='rgba(30, 30, 30, 0.8)',
                paper_bgcolor='rgba(30, 30, 30, 0)',
                yaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    zerolinecolor='rgba(128, 128, 128, 0.2)'
                ),
                xaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    zerolinecolor='rgba(128, 128, 128, 0.2)'
                ),
                font=dict(color='#ffffff'),
                showlegend=False,
                bargap=0.15,
                bargroupgap=0.1
            )
        else:
            fig.update_layout(
                title=settings['title'],
                xaxis_title='День',
                yaxis_title=settings['yaxis_title'],
                template='plotly_dark',
                height=500,
                margin=dict(t=50, b=50, l=50, r=150),
                plot_bgcolor='rgba(30, 30, 30, 0.8)',
                paper_bgcolor='rgba(30, 30, 30, 0)',
                yaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    zerolinecolor='rgba(128, 128, 128, 0.2)'
                ),
                xaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    zerolinecolor='rgba(128, 128, 128, 0.2)',
                    tickmode='linear',
                    tick0=1,
                    dtick=1
                ),
                font=dict(color='#ffffff'),
                showlegend=True,
                legend=dict(
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(30, 30, 30, 0.8)',
                    bordercolor='rgba(128, 128, 128, 0.2)',
                    borderwidth=1
                )
            )

        return fig

    def create_empty_figure():
        return go.Figure().add_annotation(
            text="Нет данных для отображения",
            showarrow=False,
            font=dict(size=20)
        )

    return dash_app