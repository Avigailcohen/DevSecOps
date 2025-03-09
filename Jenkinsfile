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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
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
                    withEnv(["DOCKER_HOST=tcp://docker-in-docker:2375"]) {
                        sh '''
                        set -e
                        echo "Running tests with pytest..."
                        docker run --rm -e PYTHONPATH=/app $IMAGE_NAME pytest || exit 1
                        '''
                    }
                }
            }
        }

        stage('Merge to Main') {
            when {
                branch 'develop'
            }
            steps {
                script {
                     withCredentials([string(credentialsId: '5274f588-fb20-4586-bfc4-88705a3fd4cd', variable: 'GIT_TOKEN')]) {
                        sh '''
                        echo "Merging develop into main..."
                        git config --global user.email "jenkins@yourdomain.com"
                        git config --global user.name "Jenkins CI"
                        git checkout main
                        git pull origin main
                        git merge --no-ff develop -m "Auto-merge develop -> main via Jenkins"
                        git push https://$GIT_USER:$GIT_PASS@github.com/Avigailcohen/DevSecOps.git main
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
