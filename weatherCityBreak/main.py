from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
import os

app = Flask('weather_service')

# Database configuration
db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_password = os.environ.get('DB_PASSWORD') or 'mypassword'
db_url = f'mysql://{db_user}:{db_password}@{db_host}/citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)

class Weathers(Resource):
    def get(self, id=None):  # GET
        city = request.args.get('city')
        date = request.args.get('date')

        query = Weather.query

        if city:
            query = query.filter(Weather.city == city)

        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(Weather.date == date)

        weathers = query.all()

        return [w.to_dict() for w in weathers]

    def post(self):
        data = request.json
        city = data.get('city')
        date = data.get('date')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        description = data.get('description')
        new_weather = Weather(city=city, date=date, temperature=temperature, humidity=humidity, description=description)
        db.session.add(new_weather)
        db.session.commit()
        return 'Ok', 201

    def put(self, id):
        weather = Weather.query.get(id)
        if weather:
            data = request.json
            weather.city = data.get('city', weather.city)
            weather.date = datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else weather.date
            weather.temperature = data.get('temperature', weather.temperature)
            weather.humidity = data.get('humidity', weather.humidity)
            weather.description = data.get('description', weather.description)
            db.session.commit()
            return {'success': 'Weather updated'}, 200
        else:
            return {'error': 'Weather not found'}, 404

    def delete(self, id):
        weather = Weather.query.get(id)
        if weather:
            db.session.delete(weather)
            db.session.commit()
            return {'success': 'Weather deleted'}, 200
        else:
            return {'error': 'Weather not found'}, 404

api.add_resource(Weathers, '/weather', '/weather/<int:id>')

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def to_dict(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else None
        return {
            'id': self.id,
            'city': self.city,
            'date': date_str,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description
        }

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
