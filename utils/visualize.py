from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import json

def create_dash_app(server):
    # Создаем экземпляр Dash
    dash_app = Dash(__name__, 
                    server=server, 
                    routes_pathname_prefix='/dash/',
                    external_stylesheets=['/static/main.css'])
    
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
            # Выпадающий список для выбора параметра
            dcc.Dropdown(
                id='parameter-selector',
                options=[
                    {'label': 'Температура', 'value': 'temperature'},
                    {'label': 'Влажность', 'value': 'humidity'},
                    {'label': 'Скорость ветра', 'value': 'wind_speed'},
                    {'label': 'Вероятность дождя', 'value': 'rain_prob'}
                ],
                value='temperature',  # значение по умолчанию
                style={'width': '300px', 'margin': '20px auto'}
            ),
            # Основной график
            dcc.Graph(id='main-graph'),
            # Контейнер для всех графиков
            html.Div([
                dcc.Graph(id='temperature-graph', style={'width': '50%', 'display': 'inline-block'}),
                dcc.Graph(id='humidity-graph', style={'width': '50%', 'display': 'inline-block'}),
                dcc.Graph(id='wind-graph', style={'width': '50%', 'display': 'inline-block'}),
                dcc.Graph(id='rain-graph', style={'width': '50%', 'display': 'inline-block'})
            ], id='all-graphs', style={'display': 'none'})
        ], className='graphs-container')
    ])

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
        [Input('parameter-selector', 'value')]
    )
    def update_main_graph(selected_param):
        data = load_weather_data()
        if not data or len(data) < 2:
            return create_empty_figure()

        settings = graphs_settings[selected_param]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[data[0]['location'], data[1]['location']],
            y=[data[0][selected_param], data[1][selected_param]],
            mode='lines+markers',
            name=settings['title'],
            line=dict(color=settings['color'], width=3),
            marker=dict(size=10)
        ))

        fig.update_layout(
            title=settings['title'],
            yaxis_title=settings['yaxis_title'],
            template='plotly_dark',
            height=500,
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=False,
            plot_bgcolor='rgba(30, 30, 30, 0.8)',
            paper_bgcolor='rgba(30, 30, 30, 0)',
            yaxis=dict(gridcolor='rgba(128, 128, 128, 0.2)', zerolinecolor='rgba(128, 128, 128, 0.2)'),
            xaxis=dict(gridcolor='rgba(128, 128, 128, 0.2)', zerolinecolor='rgba(128, 128, 128, 0.2)'),
            font=dict(color='#ffffff')
        )

        return fig

    def create_empty_figure():
        return go.Figure().add_annotation(
            text="Нет данных для отображения",
            showarrow=False,
            font=dict(size=20)
        )

    return dash_app