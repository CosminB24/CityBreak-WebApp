from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

EVENTS_SERVICE_URL = 'http://localhost:5000/search_event'
WEATHER_SERVICE_URL = 'http://localhost:5001/search_weather'

@app.route('/data', methods=['GET'])
def get_data():
    city = request.args.get('city')
    date = request.args.get('date')

    events = {}
    weather = {}

    try:
        events_response = requests.get(EVENTS_SERVICE_URL, params={'city': city, 'start_date': date, 'end_date': date})
        if events_response.status_code == 200:
            events = events_response.json()
        else:
            events = {'error': f'Could not fetch events data. Status code: {events_response.status_code}'}
    except requests.exceptions.RequestException as e:
        events = {'error': f'Request failed: {e}'}
    except ValueError as e:
        events = {'error': f'Error parsing events response: {e}'}

    try:
        weather_response = requests.get(WEATHER_SERVICE_URL, params={'city': city, 'date': date})
        if weather_response.status_code == 200:
            weather = weather_response.json()
        else:
            weather = {'error': f'Could not fetch weather data. Status code: {weather_response.status_code}'}
    except requests.exceptions.RequestException as e:
        weather = {'error': f'Request failed: {e}'}
    except ValueError as e:
        weather = {'error': f'Error parsing weather response: {e}'}

    return jsonify({
        'events': events,
        'weather': weather
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
