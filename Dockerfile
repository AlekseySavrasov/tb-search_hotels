FROM python:3.7.9-slim-stretch

RUN mkdir /bot

COPY requirements.txt /bot/

RUN python -m pip install -r /bot/requirements.txt

COPY . /bot

WORKDIR /bot

ENTRYPOINT ["python", "main.py"]
