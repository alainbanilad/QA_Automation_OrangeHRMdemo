pipeline {
    agent {
        // MAINTAINER: Dockerfile.jenkins builds a python:3.11-slim image extended with
        //   Google Chrome, OpenJDK 17, and the Allure CLI.
        //   Jenkins rebuilds the image automatically whenever Dockerfile.jenkins changes.
        //   Requires the Docker Pipeline plugin and Docker daemon on the Jenkins agent.
        dockerfile {
            filename 'Dockerfile.jenkins'
            args '-u root'
        }
    }

    // pollSCM checks the repository for new commits on a schedule.
    // This is used instead of a GitHub webhook because Jenkins is running locally
    // (http://localhost:8080) and is not reachable from the internet.
    // MAINTAINER: 'H/5 * * * *' = poll every 5 minutes. Increase the interval
    //   (e.g. 'H/15 * * * *') to reduce GitHub API calls on a slow machine.
    //   If you later expose Jenkins publicly, replace pollSCM with a webhook
    //   and remove this block.
    // MAINTAINER: 'H 2 * * *' = daily at ~2 AM agent time — triggers regression stage.
    triggers {
        pollSCM('H/5 * * * *')
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
                    # FR-012: Verify installed packages have no dependency conflicts.
                    pip check
                    echo "Dependency preflight check passed"
                '''
            }
        }

        stage('Smoke Tests') {
            steps {
                sh '''
                    set -e
                    . $VENV/bin/activate
                    # SC-002: Track smoke suite wall-clock time (target: under 600s).
                    # Using POSIX date +%s arithmetic (bash SECONDS builtin is not
                    # available under /bin/sh on Debian slim).
                    SMOKE_START=$(date +%s)
                    # MAINTAINER: Smoke scope is controlled by the -m marker expression below.
                    # To change which tests count as smoke, update @pytest.mark.smoke in the
                    # test files, or adjust the expression here. Change one side only.
                    pytest -m "smoke and orangehrm" \
                        --html=report.html \
                        --self-contained-html \
                        --alluredir=allure-results
                    SMOKE_ELAPSED=$(( $(date +%s) - SMOKE_START ))
                    echo "Smoke suite completed in ${SMOKE_ELAPSED}s (SC-002 target: under 600s)"
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
                        # MAINTAINER: Regression scope = all OrangeHRM tests plus any regression-only tests.
                        # Add @pytest.mark.orangehrm to include a test here.
                        # Add @pytest.mark.regression (without orangehrm) for regression-only tests.
                        # Widen/narrow the -m expression here to change coverage.
                        pytest -m "orangehrm or regression" \
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