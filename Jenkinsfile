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

       pipeline {
    agent any

    environment {
        IMAGE_NAME = 'appproject'
        CONTAINER_NAME = 'url-shorter'
        REPO_URL = 'https://github.com/Avigailcohen/DevSecOps.git'
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

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    echo "Building Docker image..."
                    docker build -t $IMAGE_NAME .
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                    echo "Running tests with pytest..."
                    docker run --rm -e PYTHONPATH=/app $IMAGE_NAME pytest
                    '''
                }
            }
        }

        stage('Merge to Main') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
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
    }
}

}
