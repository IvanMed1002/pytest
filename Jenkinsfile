pipeline {
    agent any

    environment {
        // Where we will store reports
        REPORT_DIR = "reports"
        VENV_DIR   = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python venv') {
            steps {
                bat """
                python --version
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Static Analysis (Lint + Security)') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                rem Lint (style / basic code issues)
                flake8 . --count --statistics --exit-zero > %REPORT_DIR%\\flake8.txt

                rem Security scan (common Python security issues)
                bandit -r . -f txt -o %REPORT_DIR%\\bandit.txt || exit /b 0
                """
            }
        }

        stage('Test + Coverage') {
            steps {
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if not exist %REPORT_DIR% mkdir %REPORT_DIR%

                rem JUnit XML for Jenkins + Coverage XML
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

                rem Option A (simple): zip the project as an artifact
                powershell -NoProfile -Command "Compress-Archive -Path * -DestinationPath %REPORT_DIR%\\project_artifact.zip -Force"

                rem Option B (real Python artifact): build wheel/sdist (requires 'build' in requirements.txt)
                python -m build || exit /b 0
                """
            }
        }
    }

    post {
        always {
            // Publish test results in Jenkins (JUnit plugin)
            junit allowEmptyResults: true, testResults: "${REPORT_DIR}/junit.xml"

            // Archive reports + artifacts so you can download them
            archiveArtifacts artifacts: "${REPORT_DIR}/**", allowEmptyArchive: true
            archiveArtifacts artifacts: "dist/**", allowEmptyArchive: true

            // Nice-to-have: show flake8/bandit logs in Jenkins build artifacts
            echo "Build finished. Reports archived."
        }

        success {
            echo "✅ SUCCESS: Tests passed and reports published."
        }

        failure {
            echo "❌ FAILURE: Something failed. Check console output + archived reports."
        failure {
            emailext(
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build failed. Check ${env.BUILD_URL}",
                to: "youremail@example.com"
            )
        }
        
