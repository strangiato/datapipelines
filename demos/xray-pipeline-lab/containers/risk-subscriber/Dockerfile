FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt risk-subscriber.py

RUN pip install -r requirements.txt

CMD ["python", "-u", "risk-subscriber.py"]
