pipeline {
    agent any

    environment {
        PYTHON = "/opt/homebrew/bin/python3.13"
        VENV = "venv"
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {

        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                echo "===== Environment ====="
                echo "PATH=$PATH"

                echo ""
                echo "Python:"
                command -v $PYTHON
                $PYTHON --version

                echo ""
                echo "Node:"
                command -v node
                node --version

                echo ""
                echo "NPM:"
                command -v npm
                npm --version

                echo ""
                echo "Newman:"
                command -v newman
                newman --version
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                rm -rf $VENV

                $PYTHON -m venv $VENV

                $VENV/bin/python3.13 --version

                $VENV/bin/python3.13 -m pip install --upgrade pip
                $VENV/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Start Flask Server') {
            steps {
                sh '''
                nohup $VENV/bin/python3.13 app.py > flask.log 2>&1 &
                sleep 5
                '''
            }
        }

        stage('Run Newman Integration Tests') {
            steps {
                sh '''
                newman run collection.json
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