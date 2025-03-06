

FROM python:3.10 AS flask

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Werkzeug===2.2.2



COPY . /app/




EXPOSE 5000

CMD ["python", "app.py"]
