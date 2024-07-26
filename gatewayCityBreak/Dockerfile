FROM python

ENV EVENTS_SERVICE_URL=localhost
ENV WEATHER_SERVICE_URL=localhost

ENV DB_HOST=auth-db
ENV DB_USER=auth
ENV DB_PASSWORD=abc123

ADD . /Project/gateway
WORKDIR /Project/gateway

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]