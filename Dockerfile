FROM python

ENV DB_HOST=172.17.0.2
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword

ADD . /eventCityBreak
WORKDIR /eventCityBreak

RUN pip install -r eventCityBreak/requirements.txt

EXPOSE 5000
CMD ["python", "eventCityBreak/main.py"]
