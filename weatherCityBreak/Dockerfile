FROM python

ENV REDIS_HOST=redis

ADD . /Project/weather
WORKDIR /Project/weather

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]