pipeline {
    agent any

    environment {
        IMAGE_NAME = 'appproject'
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

       /* stage('Merge to Main') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'github-token', variable: 'GIT_TOKEN')]) {
                        sh '''
                        echo "Merging develop into main..."
                        git config --global user.email "jenkins@yourdomain.com"
                        git config --global user.name "Jenkins CI"

                        # הגדרת Authentication ל-GitHub באמצעות ה-TOKEN
                        git remote set-url origin https://$GIT_TOKEN@github.com/Avigailcohen/DevSecOps.git

                        # ודא שהבראנץ' develop קיים מקומית
                        git fetch origin develop:develop
                        git checkout develop
                        git pull origin develop

                        # מעבר ל-main ועדכון
                        git checkout main
                        git pull --rebase origin main
                        git reset --hard origin/main

                        # מיזוג develop ל-main
                        git merge --no-ff develop -m "Auto-merge develop -> main via Jenkins"

                        # דחיפת השינויים ל-GitHub
                        git push origin main
                        '''
                    }
                }
            }
        }*/

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
