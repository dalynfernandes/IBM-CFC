from flask import Flask, jsonify, render_template, request
import pandas as pd
import requests
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complaints')  # New route for the complaints page
def complaints():
    return render_template('complaints.html')

@app.route('/actions')  # New route for the actions page
def actions():
    return render_template('actions.html')


@app.route('/get_population_image', methods=['GET'])
def get_population_image():
    return app.send_static_file('flood.png')  # Serve the PNG file

@app.route('/get_second_chart_image', methods=['GET'])
def get_second_chart_image():
    return app.send_static_file('blockage.png')  # Serve the second PNG file


@app.route('/get_population_data', methods=['GET'])
def get_population_data():
    try:
        df = pd.read_csv('population.csv')
        data = df.to_dict(orient='records')
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_weather_by_coords', methods=['POST'])
def get_weather_by_coords():
    try:
        # Get latitude and longitude from the request
        data = request.json
        lat = data['lat']
        lon = data['lon']

        # OpenWeather API call
        api_key = 'af3fb9ad8492b04468c268f2958680ce'  # Your API key
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
        
        response = requests.get(api_url)
        weather_data = response.json()

        # Extract relevant information
        weather = {
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }
        
        return jsonify(weather), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/get_gis_data', methods=['GET'])
def get_gis_data():
    # Placeholder for GIS data handling
    gis_data = {
        "locations": [
            {"lat": 40.709, "lng": -74.010, "info": "Fulton Street, NYC"},
            # Add more GIS data as needed
        ]
    }
    return jsonify(gis_data), 200

if __name__ == '__main__':
    app.run(debug=True)
