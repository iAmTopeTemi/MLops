pipeline {
    agent any
    environment {
        MLFLOW_TRACKING_URI = 'https://adb-4386313665674584.4.azuredatabricks.net'
        DATABRICKS_TOKEN = credentials('databricks-token')
    }
    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Dependencies...'
                script {
                    sh '''
                    # rm -rf .venv

                     sudo apt install python3.8-venv
                    
                    # Activate the virtual environment
                    . .venv/bin/activate

                    # .venv/bin/pip install --upgrade pip setuptools
                    
                    # Install necessary dependencies
                    # .venv/bin/pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Model Retrieve') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Retrieving Model from MLflow...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        def run_id = sh(script: '.venv/bin/python3 retrieve_model_mlflow.py', returnStdout: true).trim()
                        echo "Captured RUN ID: ${run_id}"
                        env.MLFLOW_RUN_ID = run_id
                        sh 'ls'
                    }
                }
            }
        }
        stage('Model Deploy') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Deploying to Development environment...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''                        
                        # Run the deployment script
                        # .venv/bin/python3 deploy_to_azure_ml.py
                        '''
                    }
                }
            }
        }
        stage('Model Test') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Testing deployed model...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''
                        # Run the deployment script
                        # .venv/bin/python3 model_test.py
                        '''
                    }
                }
            }
        }
        stage('Set Challenger Alias') {
            steps {
                script {
                    // withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    withEnv(["DATABRICKS_HOST=${env.MLFLOW_TRACKING_URI}", "DATABRICKS_TOKEN=${env.DATABRICKS_TOKEN}", "MLFLOW_RUN_ID=${env.MLFLOW_RUN_ID}"]) {
                        echo "RUN ID for Registration: ${env.MLFLOW_RUN_ID}"  // Debugging line
                        sh 'echo $MLFLOW_RUN_ID'  // Debugging line
                        sh '.venv/bin/python3 dev/update_model_tag.py'
                    }
                }
            }
        }
        stage('Save Model') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Saving Model to ADLS...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''                        
                        # Run the training script
                        # .venv/bin/python3 save_model_to_ADLS.py
                        '''
                    }
                }
            }
        }
        stage('Destroy') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Destroying web service for deployed model...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''                       
                        # Run the deployment script
                        # .venv/bin/python3 destroy_web_service.py
                        '''
                    }
                }
            }
        }
        stage('Deploy to Preprod') {
            when {
                // Check if the branch is 'main'
                branch 'main'
            }
            steps {
                echo 'Deploying to Preproduction environment...'
            }
        }
        stage('Deploy to Production') {
            when {
                // Check if the branch is 'main' and contains a tag with 'release' prefix
                allOf {
                    branch 'main'
                    tag 'release/*'
                }
            }
            steps {
                echo 'Deploying to Production environment...'
            }
        }
    }
}
