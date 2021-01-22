FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt anon-processor.py ./

RUN pip install -r requirements.txt

CMD ["python", "-u", "anon-processor.py"]
