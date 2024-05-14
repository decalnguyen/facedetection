FROM python

WORKDIR /app

COPY requirements.txt ./

COPY haarcascade_frontalface_default.xml ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]