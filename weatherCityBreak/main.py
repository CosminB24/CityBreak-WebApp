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
    return render_template('search_weather.html')


@app.route('/search_weather')
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
        query = query.filter(Weather.date >= start_date)

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

@app.route('/weather/update/<int:weather_id>', methods=['POST'])
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

@app.route('/weather/delete/<int:weather_id>', methods=['POST'])
def delete_weather(weather_id):
    weather = Weather.query.get(weather_id)
    if weather:
        db.session.delete(weather)
        db.session.commit()
        return redirect(url_for('weather_results'))
    else:
        return "Weather not found", 404

class Weathers(Resource):
    def get(self, id=None):
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

api.add_resource(Weathers, '/api/weather', '/api/weather/<int:id>')

class Weather(db.Model):
    #ID, city, date, temperature, humidity, description
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)