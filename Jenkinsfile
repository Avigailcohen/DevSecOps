pipeline {
    agent any

    environment {
        IMAGE_NAME = 'avigacoh/appproject' // 🔹 עדכון לשם המשתמש שלך ב-Docker Hub
        CONTAINER_NAME = 'url-shorter'
        REPO_URL = 'https://github.com/Avigailcohen/DevSecOps.git'
        DOCKER_HOST = 'tcp://docker-in-docker:2375' // 🔹 שימוש ב-DIND
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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
                        sh '''
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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
                        sh '''
                        echo "Building Docker image..."
                        docker build -t $IMAGE_NAME .
                        '''
                    }
                }
            }
        }

        stage('Push to Docker Hub') { // 🔹 שלב חדש להעלאה ל-Docker Hub
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                        echo "Logging in to Docker Hub..."
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        echo "Pushing Docker image to Docker Hub..."
                        docker push $IMAGE_NAME
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
                        sh '''
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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
                        sh '''
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
