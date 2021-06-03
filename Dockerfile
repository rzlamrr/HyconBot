FROM python:3-slim-buster

COPY . .

RUN pip3 install -U -r requirements.txt

CMD python3 -m hycon