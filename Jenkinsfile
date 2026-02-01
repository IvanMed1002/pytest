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
                bat 'python --version'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'python -m pytest --junitxml=reports\\junit.xml'
            }
        }

        stage('Code Coverage') {
            steps {
                bat 'pip show coverage || pip install coverage'
                bat 'coverage run -m pytest'
                bat 'coverage xml -o reports\\coverage.xml'
                bat 'coverage report'
            }
        }

        stage('Static Code Analysis') {
            steps {
                bat 'pip show pylint || pip install pylint'
                bat 'pylint *.py || exit /b 0'
            }
        }

        stage('Artifact') {
            steps {
                bat 'powershell -Command "Compress-Archive -Path *.py -DestinationPath artifact.zip -Force"'
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**, artifact.zip', fingerprint: true
        }
        success {
            echo 'SUCCESS ✅'
        }
        failure {
            echo 'FAILED ❌'
        }
    }
}
