from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import request, redirect, url_for
from datetime import datetime

import os

app = Flask('assignment')


#docker run --name CitybreakDB -e MYSQL_ROOT_PASSWORD=myrootpw -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword -e MYSQL_DATABASE=citybreak -p 3306:3306 -d mysql
db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_password = os.environ.get('DB_PASSWORD') or 'mypassword'


db_url = f'mysql://{db_user}:{db_password}@{db_host}/citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)

@app.route('/')
def index():
    return render_template('search_events.html')

@app.route('/search_events')
def search_events():
    return render_template('search_events.html')

@app.route('/event')
def event_results():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    current_date = datetime.now().date()  # Get the current date

    query = Event.query.filter(Event.date >= current_date)  # Ensure events are not in the past

    if city:
        query = query.filter(Event.city == city)

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Event.date >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Event.date <= end_date)

    events = query.all()

    return render_template('events.html', events=events)


@app.route('/previous_events')
def previous_events():
    city = request.args.get('city')
    current_date = datetime.now().date()

    if city:
        events = Event.query.filter(Event.city == city, Event.date > current_date).all()
    else:
        events = Event.query.filter(Event.date < current_date).all()
    return render_template('previous_events.html', events=events)


'''@app.route('/search_weather')
def search_weather():
    return render_template('search_weather.html')

@app.route('/weather')
def weather_results():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    current_date = datetime.now().date()

    query = Weather.query.filter(Weather.date >= current_date)

    if city:
        query = query.filter(Weather.city == city)

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Event.date >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Weather.date <= end_date)

    weathers = query.all()

    return render_template('weather.html', weathers=weathers)


@app.route('/weather/create', methods=['GET'])
def create_weather_form():
    return render_template('create_weather.html')

@app.route('/weather/create', methods=['POST'])
# ID, city, date, temperature, humidity, description
def create_weather():
    city = request.form['city']
    date = request.form['date']
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    description = request.form['description']

    new_weather = Weather(city=city, date=date, temperature=temperature, humidity=humidity, description=description)
    db.session.add(new_weather)
    db.session.commit()

    return redirect(url_for('weather_results'))

@app.route('/weather/edit/<int:weather_id>')
def edit_weather(weather_id):
    weather = Weather.query.get(weather_id)
    if weather:
        return render_template('edit_weather.html', weather=weather)
    else:
        return "Weather not found", 404
'''
'''@app.route('/weather/update/<int:weather_id>', methods=['POST'])
def update_weather(weather_id):
    weather = Weather.query.get(weather_id)
    if weather:
        weather.city = request.form['city']
        weather.date = request.form['date']
        weather.temperature = request.form['temperature']
        weather.humidity = request.form['humidity']
        weather.description = request.form['description']
        db.session.commit()
        return redirect(url_for('weather_results'))
    else:
        return "Weather not found",
'''
'''@app.route('/weather/delete/<int:weather_id>', methods=['POST'])
def delete_weather(weather_id):
    weather = Weather.query.get(weather_id)
    if weather:
        db.session.delete(weather)
        db.session.commit()
        return redirect(url_for('weather_results'))
    else:
        return "Weather not found", 404
'''
@app.route('/event/update/<int:event_id>', methods=['POST'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event:
        event.city = request.form['city']
        event.date = request.form['date']
        event.title = request.form['title']
        event.description = request.form['description']
        db.session.commit()
        return redirect(url_for('event_results'))
    else:
        return "Event not found",


@app.route('/event/create', methods=['GET'])
def create_event_form():
    return render_template('create_event.html')

@app.route('/event/create', methods=['POST'])
def create_event():
    city = request.form['city']
    date = request.form['date']
    title = request.form['title']
    description = request.form['description']

    new_event = Event(city=city, date=date, title=title, description=description)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('event_results'))

@app.route('/event/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('event_results'))
    else:
        return "Event not found", 404


class Events(Resource):
    def get(self, id=None):  # GET
        if id:
            event = Event.query.get(id)
            if event:
                return event.to_dict()
            else:
                return {'error': 'Event not found'}, 404
        else:
            events = Event.query.all()
            return [e.to_dict() for e in events]


    def post(self):
        # ID, city, date, title, description
        data = request.json
        id = data.get('id')
        city = data.get('city')
        date = data.get('date')
        title = data.get('title')
        description = data.get('description')
        e = Event(id=id, city=city, date=date, title=title, description=description)
        db.session.add(e)
        db.session.commit()
        return 'Ok', 201


    def put(self, id=None):
        if id:
            event = Event.query.get(id)
            if event:
                data = request.json
                event.city = data.get('city', event.city)
                event.date = data.get('date', event.date)
                event.title = data.get('title', event.title)
                event.description = data.get('description', event.description)
                db.session.commit()
                return {'success' : 'Event update'}, 200
            else:
                return {'error' : 'Event not found'}, 404
        else:
            return {'error' : 'ID not found'}, 404

    def delete(self, id=None):
        if id:
            event = Event.query.get(id)
            if event:
                db.session.delete(event)
                db.session.commit()
                return {'success': 'The event was removed'}, 200
            else:
                return {'error': 'Event not found'}, 404
        else:
            return {'error': 'ID is required'}, 400

'''class Weathers(Resource):
    def get(self, id=None):  # GET
        if id:
            weather = Weather.query.get(id)
            if weather:
                return weather.to_dict()
            else:
                return {'error': 'option not found'}, 404
        else:
            weathers = Weather.query.all()
            return [w.to_dict() for w in weathers]


    def post(self):
        #ID, city, date, temperature, humidity, description
        data = request.json
        id = data.get('id')
        city = data.get('city')
        date = data.get('date')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        description = data.get('description')
        w = Weather(id=id, city=city, date=date, temperature=temperature, humidity=humidity, description=description)
        db.session.add(w)
        db.session.commit()
        return 'Ok', 201


    def put(self, id=None):
        # ID, city, date, temperature, humidity, description
        if id:
            weather = Weather.query.get(id)
            if weather:
                data = request.json
                weather.city = data.get('city', weather.city)
                weather.date = data.get('date', weather.date)
                weather.temperature = data.get('temperature', weather.temperature)
                weather.humidity = data.get('humidity', weather.humidity)
                weather.description = data.get('description', weather.description)
                db.session.commit()
                return {'success' : 'weather updated'}, 200
            else:
                return {'error' : 'option not found'}, 404
        else:
            return {'error' : 'ID not found'}, 404


    def delete(self, id=None):
        if id:
            weather = Weather.query.get(id)
            if weather:
                db.session.delete(weather)
                db.session.commit()
                return {'success' : 'option deleted'}, 200
            else:
                return {'error' : 'invalid ID'}, 404
        else:
            return {'error' : 'ID is required'}
'''
api.add_resource(Events, '/api/event', '/api/event/<int:id>')
#api.add_resource(Weathers, '/api/weather', '/api/weather/<int:id>')


class Event(db.Model):
    #ID, city, date, title, description
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))

    def to_dict(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else None
        return {
            'id': self.id,
            'city': self.city,
            'date': date_str,
            'title': self.title,
            'description': self.description
        }


'''class Weather(db.Model):
    ID, city, date, temperature, humidity, description
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def to_dict(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else None
        return{
        'id': self.id,
        'city': self.city,
        'date': date_str,
        'temperature': self.temperature,
        'humidity': self.humidity,
        'description': self.description
        }
'''
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
