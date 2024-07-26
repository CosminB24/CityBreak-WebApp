from flask import Flask, request, render_template
from flask_session import Session
from flask_restful import Resource, Api

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

import json
import os
import logging
import datetime
import time

app = Flask('events')
DB_USER = os.environ.get('DB_USER') or 'event'
DB_PASS = os.environ.get('DB_PASSWORD') or 'abc123'
DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'  #prin 127.0.0.1 se conecteaza prin TCP, daca e localhost, se conecteaza prin sockets
PORT = int(os.environ.get('PORT') or 5000)
HOST = os.environ.get('HOST') or '0.0.0.0'

db_url = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/citybreak'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

api = Api(app)
time.sleep(30)
db = SQLAlchemy(app)

class Events(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        events = db.session.query(Event)
        if city:
            events = events.filter(Event.city == city)
        if date:
            events = events.filter(Event.date == date)
        return [e.to_dict() for e in events.all()], 200

    def put(self):
        event_id = request.form.get('id')
        if not event_id:
            return 'Event ID missing', 401 #TODO check HTTP error codes
        try:
            event_id = int(event_id)
        except ValueError as e:
            return 'Invalid ID', 401
        city = request.form.get('city')
        name = request.form.get('name')
        description = request.form.get('description')
        date = request.form.get('date')
        date = datetime.date(*[int(s) for s in date.split('-')]) if date else datetime.date.today()
        event = db.session.query(Event).filter(Event.id==event_id)
        if event:
            event = event.first()
            event.city = city if city else event.city
            event.name = name if name else event.name
            event.description = description if description else event.description
            event.date = date if date else event.date
            db.session.commit()
            return 'Ok', 201
        return 'Not found', 401

    def post(self):
        city = request.form.get('city', 'Brasov')
        name = request.form.get('name')
        description = request.form.get('description')
        date = request.form.get('date')
        date = datetime.date(*[int(s) for s in date.split('-')]) if date else None
        event = Event(city=city, name=name, description=description, date=date)
        db.session.add(event)
        db.session.commit()
        return event.id, 201

    def delete(self):
        pass

api.add_resource(Events, '/events')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128)) #varchar
    date = db.Column(db.Date)
    name = db.Column(db.String(256))
    description = db.Column(db.Text) #text = nelimitat, nu are un anumit numar de parametri, precum String

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                d[k] = self.__dict__[k] if 'date' not in k else str(self.__dict__[k])
        return d

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)