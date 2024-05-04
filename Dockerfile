FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt requirments.txt

RUN pip3 install -r requirements.txt

COPY ..

CMD ["python3", "main.py"]