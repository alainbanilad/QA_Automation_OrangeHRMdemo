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
                pytest -m "smoke and orangehrm" --html=report.html --self-contained-html
                '''
            }
        }

        stage('Allure Report') {
            steps {
                sh '''
                . $VENV/bin/activate
                pytest -m "smoke and orangehrm" --alluredir=allure-results
                allure generate allure-results -o allure-report --clean
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', onlyIfSuccessful: false
        }
        failure {
            echo '❌ Tests failed'
        }
        success {
            echo '✅ Tests passed'
        }
    }

}