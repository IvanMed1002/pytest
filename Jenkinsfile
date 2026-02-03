pipeline {
    agent any

    environment {
        REPORT_DIR = "reports"
        VENV_DIR   = ".venv"
        // Optional: set this if Jenkins can't find python in PATH
        // PY = "C:\\Users\\Ivan\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        PY = "python"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

     stage('Setup Python venv') {
         steps {
             bat '''
             py --version
             py -m venv .venv
             call .venv\\Scripts\\activate
             py -m pip install --upgrade pip
             py -m pip install -r requirements.txt
             '''
         }
     }    


        stage('Static Analysis (Lint + Security)') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                rem Lint
                flake8 . --count --statistics --exit-zero > %REPORT_DIR%\\flake8.txt

                rem Security scan
                bandit -r . -f txt -o %REPORT_DIR%\\bandit.txt || exit /b 0
                """
            }
        }

        stage('Test + Coverage') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                pytest -q ^
                  --junitxml=%REPORT_DIR%\\junit.xml ^
                  --cov=. ^
                  --cov-report=xml:%REPORT_DIR%\\coverage.xml ^
                  --cov-report=html:%REPORT_DIR%\\htmlcov
                """
            }
        }

        stage('Build Artifact') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate

                powershell -NoProfile -Command "Compress-Archive -Path * -DestinationPath %REPORT_DIR%\\project_artifact.zip -Force"

                rem Build wheel/sdist if 'build' is installed
                python -m build || exit /b 0
                """
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: "reports/junit.xml"
            archiveArtifacts artifacts: "reports/**", allowEmptyArchive: true
            archiveArtifacts artifacts: "dist/**", allowEmptyArchive: true
            echo "Build finished. Reports archived."
        }

        success {
            echo "SUCCESS ✅"
            // Slack only works if Slack plugin is installed + configured in Jenkins
            // slackSend(message: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}", channel: "#all-project")
        }

        failure {
            echo "FAILED ❌"
            // slackSend(message: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}", channel: "#all-project")
        }
    }
}
