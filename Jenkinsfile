pipeline {
    agent any

    environment {
        IMAGE_NAME = 'appproject'
        CONTAINER_NAME = 'url-shorter'
        REPO_URL = 'https://github.com/Avigailcohen/DevSecOps.git'
        DOCKER_HOST = 'tcp://docker-in-docker:2375' // 🔹 הגדרת החיבור לדוקר
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    deleteDir()
                    checkout scm
                }
            }
        }

        stage('Clean Up Old Containers') {
            steps {
                script {
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) { // 🔹 שימוש ב-DIND
                        sh '''
                        set -e
                        echo "Cleaning up old containers..."
                        docker ps -q --filter "name=$CONTAINER_NAME" | xargs -r docker stop | xargs -r docker rm
                        docker container prune -f
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) { // 🔹 שימוש ב-DIND
                        sh '''
                        set -e
                        echo "Building Docker image..."
                        docker build -t $IMAGE_NAME .
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) { // 🔹 שימוש ב-DIND
                        sh '''
                        set -e
                        echo "Running tests with pytest..."
                        docker run --rm -e PYTHONPATH=/app $IMAGE_NAME pytest || exit 1
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) { // 🔹 שימוש ב-DIND
                        sh '''
                        set -e
                        echo "Deploying Flask App on port 5000..."
                        docker ps -q --filter "name=$CONTAINER_NAME" | xargs -r docker stop | xargs -r docker rm
                        docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                        '''
                    }
                }
            }
        }
    }
}
