from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
import os

app = Flask('events_service')

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_password = os.environ.get('DB_PASSWORD') or 'mypassword'
db_url = f'mysql://{db_user}:{db_password}@{db_host}/citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)

class Events(Resource):
    def get(self, id=None):  # GET
        city = request.args.get('city')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        current_date = datetime.now().date()

        query = Event.query.filter(Event.date >= current_date)

        if city:
            query = query.filter(Event.city == city)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Event.date >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Event.date <= end_date)

        events = query.all()

        return [e.to_dict() for e in events]

    def post(self):
        data = request.json
        city = data.get('city')
        date = data.get('date')
        title = data.get('title')
        description = data.get('description')
        new_event = Event(city=city, date=date, title=title, description=description)
        db.session.add(new_event)
        db.session.commit()
        return 'Ok', 201

    def put(self, id):
        event = Event.query.get(id)
        if event:
            data = request.json
            event.city = data.get('city', event.city)
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else event.date
            event.title = data.get('title', event.title)
            event.description = data.get('description', event.description)
            db.session.commit()
            return {'success': 'Event updated'}, 200
        else:
            return {'error': 'Event not found'}, 404

    def delete(self, id):
        event = Event.query.get(id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return {'success': 'The event was removed'}, 200
        else:
            return {'error': 'Event not found'}, 404

api.add_resource(Events, '/event', '/event/<int:id>')

class Event(db.Model):
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

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
