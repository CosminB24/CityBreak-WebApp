FROM python

ENV DB_HOST=localhost
ENV DB_USER=event
ENV DB_PASSWORD=abc123
ENV PORT=5000
ENV HOST=0.0.0.0

ADD . /CityBreakDemonstration/events
WORKDIR /CityBreakDemonstration/events

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]