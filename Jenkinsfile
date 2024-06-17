pipeline {
    agent any
    environment {
        MLFLOW_TRACKING_URI = 'https://adb-1466274833195066.6.azuredatabricks.net'
        DATABRICKS_TOKEN = credentials('databricks-token')
    }
    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Dependencies...'
                script {
                    sh '''
                     rm -rf .venv

                     python3.12 -m venv .venv
                    
                    # Activate the virtual environment
                     . .venv/bin/activate

                     .venv/bin/pip install --upgrade pip setuptools
                    
                    # Install necessary dependencies
                     .venv/bin/pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Model Train') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Training and registering model...'
                script {
                    sh '''                        
                        # Run the retriever script
                        .venv/bin/python3 train_model_mlflow.py
                        '''
                }
            }
        }
        stage('Unity Catalog Retrieve') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Retrieving model catalog...'
                script {
                    sh '''                        
                        # Run the retriever script
                         .venv/bin/python3 get_unity_catalogs.py
                         .venv/bin/python3 get_catalog_schemas.py
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
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureSP')]) {
                        //def run_id = sh(script: '.venv/bin/python3 retrieve_model_mlflow.py', returnStdout: true).trim()
                        //echo "Captured RUN ID: ${run_id}"
                        //env.MLFLOW_RUN_ID = run_id
                        sh 'pwd'
                    }
                }
            }
        }
        stage('Model Retrieve and Deploy') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Deploying to Development environment...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureSP')]) {
                        sh '''                        
                        # Run the deployment script
                         .venv/bin/python3 deploy_model_to_azure.py
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
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureSP')]) {
                        sh '''
                        # Run the deployment script
                         .venv/bin/python3 model_test.py
                        '''
                    }
                }
            }
        }
        stage('Set Challenger Alias') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                script {
                    // withCredentials([string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')]) {
                    withEnv(["DATABRICKS_HOST=${env.MLFLOW_TRACKING_URI}", "DATABRICKS_TOKEN=${env.DATABRICKS_TOKEN}", "MLFLOW_RUN_ID=${env.MLFLOW_RUN_ID}"]) {
                        echo "RUN ID for Registration: ${env.MLFLOW_RUN_ID}"
                        sh 'echo $MLFLOW_RUN_ID'
                        sh '.venv/bin/python3 update_model_tag.py'
                        sh 'pwd'
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
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureSP')]) {
                        sh '''                        
                        # Run the training script
                        .venv/bin/python3 save_model_to_ADLS.py
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
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureSP')]) {
                        sh '''                       
                        # Run the deployment script
                         .venv/bin/python3 destroy_web_service.py
                        '''
                    }
                }
            }
        }
    }
}