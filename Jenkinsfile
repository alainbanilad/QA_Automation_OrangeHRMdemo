pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }


    environment {
        VENV = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 --version
                python3 -m venv $VENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests (Headless)') {
            steps {
                sh '''
                . $VENV/bin/activate
                pytest --html=report.html --self-contained-html
                '''
            }
        }

        stage('Allure Report') {
            steps {
                sh '''
                . $VENV/bin/activate
                pytest --alluredir=allure-results
                allure generate allure-results -o allure-report --clean
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', fingerprint: true
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }

        failure {
            echo '❌ Tests failed'
        }

        success {
            echo '✅ Tests passed'
        }
    }
}