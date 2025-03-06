pipeline {
    agent any

    environment {
        IMAGE_NAME = 'appproject'
        CONTAINER_NAME = 'url-shorter'
        REPO_URL = 'https://github.com/YOUR-USERNAME/YOUR-REPO.git'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    sh '''
                    echo "Checking out branch: ${env.BRANCH_NAME}"
                    git clone --depth=1 $REPO_URL .
                    git checkout ${env.BRANCH_NAME}
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Clean Up Old Containers') {
            steps {
                script {
                    sh '''
                    CONTAINER_ID=$(docker ps -q --filter "name=$CONTAINER_NAME")
                    if [ ! -z "$CONTAINER_ID" ]; then
                        echo "Stopping existing container: $CONTAINER_ID"
                        docker stop $CONTAINER_ID
                        docker rm $CONTAINER_ID
                    fi
                    docker system prune -f
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "docker run --rm -e PYTHONPATH=/app $IMAGE_NAME pytest"
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'  // רק אם אנחנו על main נבצע Deploy
            }
            steps {
                script {
                    sh '''
                    echo "Deploying Flask App..."
                    docker run -d --name $CONTAINER_NAME -p 8080:8080 $IMAGE_NAME
                    '''
                }
            }
        }
    }
}
