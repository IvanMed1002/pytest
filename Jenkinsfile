pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Code Coverage') {
            steps {
                sh '''
                coverage run -m pytest
                coverage report
                coverage xml
                '''
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh 'pylint math_utils.py || true'
            }
        }
    }
}
