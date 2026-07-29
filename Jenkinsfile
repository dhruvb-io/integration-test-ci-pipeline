pipeline {
    agent any

    environment {
        PYTHON = "/opt/homebrew/bin/python3.13"
        NODE = "/opt/homebrew/bin/node"
        NPM = "/opt/homebrew/bin/npm"
        NEWMAN = "/usr/local/bin/newman"
        VENV = "venv"
    }

    stages {

        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                $PYTHON -m venv $VENV
                . $VENV/bin/activate

                python --version
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Install Newman') {
            steps {
                sh '''
                $NPM install -g newman
                '''
            }
        }

        stage('Start Flask Server') {
            steps {
                sh '''
                . $VENV/bin/activate

                nohup python app.py > flask.log 2>&1 &
                sleep 3
                '''
            }
        }

        stage('Run Newman Integration Tests') {
            steps {
                sh '''
                $NEWMAN run collection.json
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'flask.log', allowEmptyArchive: true
        }

        success {
            echo 'API Integration Tests Passed'
        }

        failure {
            echo 'API Integration Tests Failed'
        }
    }
}