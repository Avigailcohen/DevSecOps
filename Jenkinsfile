pipeline {
    agent any

    environment {
        IMAGE_NAME = 'appproject'
        CONTAINER_NAME = 'url-shorter'
        REPO_URL = 'https://github.com/YOUR-USERNAME/YOUR-REPO.git'
        GITHUB_TOKEN = credentials('github-token') // יש להגדיר את ה-TOKEN ב-Jenkins
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

        stage('Auto Merge to Main') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    sh '''
                    echo "Merging branch ${env.BRANCH_NAME} into main"
                    git config --global user.email "jenkins@yourdomain.com"
                    git config --global user.name "Jenkins"
                    
                    git checkout main
                    git pull origin main
                    git merge --no-ff ${env.BRANCH_NAME}
                    
                    git push git@github.com:Avigailcohen/DevSecOps.git main


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
                    echo "Deploying Flask App..."
                    docker run -d --name $CONTAINER_NAME -p 8080:8080 $IMAGE_NAME
                    '''
                }
            }
        }
    }
}
