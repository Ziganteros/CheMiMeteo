from flask import Flask, render_template, request
import requests


def create_app():
    app = Flask(__name__)

    def get_weather_forecast(city):
        api_key = '14be3e2d36543d5ab9c674d4ef66696c'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        # Extracting 5-day forecast
        forecast = []
        if data.get('list'):
            for i in range(0, 40, 8):  # 8 intervals of 3 hours per day
                day_data = {
                    'date': data['list'][i]['dt_txt'].split(' ')[0],
                    'temp': data['list'][i]['main']['temp'],
                    'description': data['list'][i]['weather'][0]['description'],
                    'icon': data['list'][i]['weather'][0]['icon']
                }
                forecast.append(day_data)
        
        return forecast

    def get_clothing_recommendations(temp):
        if temp < 10:
            return ["Heavy jacket", "Scarf", "Gloves", "Warm hat"]
        elif temp < 20:
            return ["Light jacket", "Sweater", "Jeans", "Closed shoes"]
        elif temp < 30:
            return ["T-shirt", "Light pants or shorts", "Sneakers", "Light sweater"]
        else:
            return ["Shorts", "Tank top", "Sandals", "Hat and sunglasses"]

    @app.route('/', methods=['GET', 'POST'])
    def home():
        forecast = None
        city = None
        selected_day = None
        clothing_recommendations = None
        
        if request.method == 'POST':
            city = request.form.get('city')
            forecast = get_weather_forecast(city)
            
            selected_day_index = request.form.get('day')
            if selected_day_index is not None:
                selected_day_index = int(selected_day_index)
                selected_day = forecast[selected_day_index]
                clothing_recommendations = get_clothing_recommendations(selected_day['temp'])
        
        return render_template('home.html', city=city, forecast=forecast, selected_day=selected_day, clothing_recommendations=clothing_recommendations)

    return app
