FROM jenkins/jenkins:lts AS jenkins

FROM python:3.10 AS flask

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=jenkins /var/jenkins_home /var/jenkins_home

COPY . /app/

EXPOSE 8080

CMD ["python", "app.py"]
