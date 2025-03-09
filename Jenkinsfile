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
                    sh '''
                    # שימוש ב-bash כדי למנוע שגיאות תחביר
                    set -e
                    echo "Checking out branch: $BRANCH_NAME"
                    git clone --depth=1 "$REPO_URL" .
                    git checkout "$BRANCH_NAME"
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "Checking for pip..."
                    if ! command -v pip &> /dev/null; then
                        echo "pip not found! Trying to install..."
                        sudo apt-get update && sudo apt-get install -y python3-pip
                    fi
                    echo "Installing dependencies..."
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Clean Up Old Containers') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "Cleaning up old containers..."
                    docker ps -q --filter "name=$CONTAINER_NAME" | xargs -r docker stop | xargs -r docker rm
                    docker container prune -f
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    set -e
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
                    set -e
                    echo "Running tests with pytest..."
                    docker run --rm -e PYTHONPATH=/app $IMAGE_NAME pytest || exit 1
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
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
