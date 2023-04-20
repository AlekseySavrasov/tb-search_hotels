FROM python:3.10-slim
RUN mkdir /bot
COPY requirements.txt /bot/
COPY main.py /bot/
RUN python -m pip install -r /bot/requirements.txt
WORKDIR /bot
ENTRYPOINT ["python", "main.py"]
