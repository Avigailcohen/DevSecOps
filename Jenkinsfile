pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t flask-url-shortener .'
                }
            }
        }
        stage('Run Flask App') {
            steps {
                script {
                    sh 'docker run -d -p 8080:8080 flask-url-shortener'
                }
            }
        }
    }
}
