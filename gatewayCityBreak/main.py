from flask import Flask, request, jsonify, render_template
import requests

app = Flask('gateway_service')

EVENTS_SERVICE_URL = 'http://172.17.0.2:5000/event'
WEATHER_SERVICE_URL = 'http://172.17.0.2:5001/weather'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET': # and request.form['city'] is not None:
        city = None
        date = None
        if request.args.get('city', None):
            city = request.args['city']
        if request.args.get('date', None):
            date = request.args['date']


        events = {}
        weather = {}

        if city is not None and date is not None:

            try:
                events_response = requests.get(EVENTS_SERVICE_URL,
                                               params={'city': city, 'start_date': date, 'end_date': date})
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

            return render_template('results.html', city=city, date=date, events=events, weather=weather)

    return render_template('search.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
