pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    // PR builds fire automatically via Jenkins multibranch webhook / GitHub Branch Source plugin.
    // The cron entry below triggers the daily regression run on the default branch.
    // MAINTAINER: Adjust the schedule here. 'H 2 * * *' = daily at ~2 AM agent time.
    triggers {
        cron('H 2 * * *')
    }

    environment {
        VENV = 'venv'
        // MAINTAINER: The three credential IDs below must exist in
        //   Jenkins > Manage Jenkins > Credentials.
        //   Create three "Secret text" credentials and use these exact IDs,
        //   or update the IDs here to match what you have created.
        ORANGEHRM_BASE_URL = credentials('orangehrm-base-url')
        ORANGEHRM_USERNAME = credentials('orangehrm-username')
        ORANGEHRM_PASSWORD = credentials('orangehrm-password')
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
                    set -e
                    python3 --version
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Smoke Tests') {
            steps {
                sh '''
                    set -e
                    . $VENV/bin/activate
                    # MAINTAINER: Smoke scope is controlled by the -m marker expression below.
                    # To change which tests count as smoke, update @pytest.mark.smoke in the
                    # test files, or adjust the expression here. Change one side only.
                    pytest -m "smoke and orangehrm" \
                        --html=report.html \
                        --self-contained-html \
                        --alluredir=allure-results
                '''
            }
        }

        stage('Regression Tests') {
            // Regression runs on the daily scheduled build or direct pushes to the default branch.
            // Pull request builds skip this stage to keep PR feedback fast.
            when {
                anyOf {
                    triggeredBy 'TimerTrigger'
                    allOf {
                        not { changeRequest() }
                        branch 'main'
                    }
                }
            }
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    sh '''
                        set -e
                        . $VENV/bin/activate
                        # MAINTAINER: Regression scope runs all OrangeHRM tests.
                        # Add @pytest.mark.regression to any test to include it in regression-only runs,
                        # or widen/narrow the -m expression here to change coverage.
                        pytest -m "orangehrm" \
                            --html=report.html \
                            --self-contained-html \
                            --alluredir=allure-results
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    set -e
                    allure generate allure-results -o allure-report --clean
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
        }
        failure {
            echo '❌ Tests failed — screenshots and allure results are archived above'
            archiveArtifacts artifacts: 'artifacts/screenshots/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
        success {
            echo '✅ Tests passed'
        }
    }
}