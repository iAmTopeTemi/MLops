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
        stage('Model Train & Register to mlflow') {
            when {
                // Check which branch triggered the build
                branch 'dev'
            }
            steps {
                echo 'Training and registering model...'
                script {
                    sh '''                        
                        # Run the retriever script
                        .venv/bin/python3 dev_branch/train_model_mlflow.py
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
                         .venv/bin/python3 dev_branch/deploy_model_to_azure.py
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
                         .venv/bin/python3 dev_branch/model_test.py
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
                        sh '.venv/bin/python3 dev_branch/update_model_tag.py'
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
                        .venv/bin/python3 dev_branch/save_model_to_ADLS.py
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
                         .venv/bin/python3 dev_branch/destroy_web_service.py
                        '''
                    }
                }
            }
        }
         Pre Prod
        stage('Preprod - Load From ADLS') {
            when {
                // Check if the branch is 'main'
                branch 'main'
            }
            steps {
                echo 'Loading model from ADLS...'
                script {
                    sh '.venv/bin/python3 main_preprod_branch/retrieve_model_from_ADLS.py'
                }
            }
        }
        stage('Preprod - Log Model MLflow') {
            when {
                // Check if the branch is 'main'
                branch 'main'
            }
            steps {
                echo 'Logging model to MLflow...'
                script {
                    // sh '.venv/bin/python3 main_preprod_branch/log_model_to_mlflow.py'
                    def run_id = sh(script: '.venv/bin/python3 main_preprod_branch/log_model_to_mlflow.py', returnStdout: true).trim()
                    echo "Captured RUN ID: ${run_id}"
                    env.MLFLOW_RUN_ID = run_id
                }
            }
        }
        stage('Preprod - Register Model UC') {
            when {
                // Check if the branch is 'main'
                branch 'main'
            }
            steps {
                script {
                    withEnv(["MLFLOW_RUN_ID=${env.MLFLOW_RUN_ID}"]) {
                        echo "RUN ID for Registration: ${env.MLFLOW_RUN_ID}"
                        sh 'echo $MLFLOW_RUN_ID'
                        echo 'Registering model to Unity Catalog...'
                        sh '.venv/bin/python3 main_preprod_branch/register_model_uc.py'
                    }
                }
            }
        }
        stage('Preprod - Model Deploy') {
            when {
                // Check which branch triggered the build
                branch 'main'
            }
            steps {
                echo 'Deploying to pre prod environment...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''                        
                        # Run the deployment script
                        .venv/bin/python3 main_preprod_branch/deploy_model_to_azure.py
                        '''
                    }
                }
            }
        }
        stage('Preprod - Model Unit Test') {
            when {
                // Check which branch triggered the build
                branch 'main'
            }
            steps {
                echo 'Testing deployed model (unit tests)...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''
                        # Run the deployment script
                        .venv/bin/python3 main_preprod_branch/model_test.py
                        '''
                    }
                }
            }
        }
        stage('Preprod - Model Integration Test') {
            when {
                // Check which branch triggered the build
                branch 'main'
            }
            steps {
                echo 'Testing deployed model (integration test)...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''
                        # Run the deployment script
                        .venv/bin/python3 main_preprod_branch/model_test.py
                        '''
                    }
                }
            }
        }
        stage('Preprod - Upgrade Model Alias') {
            when {
                // Check which branch triggered the build
                branch 'main'
            }
            steps {
                script {
                    sh '.venv/bin/python3 main_preprod_branch/update_model_tag.py'
                    sh 'pwd'
                }
            }
        }
        stage('Preprod - Destroy') {
            when {
                // Check which branch triggered the build
                branch 'main'
            }
            steps {
                echo 'Destroying web service for deployed model...'
                script {
                    withCredentials([azureServicePrincipal(credentialsId: 'AzureServicePrincipal')]) {
                        sh '''                       
                        # Run the deployment script
                        .venv/bin/python3 main_preprod_branch/destroy_web_service.py
                        '''
                    }
                }
            }
        }

        // Prod
        // stage('Deploy to Production') {
        //     when {
        //         // Check if the branch is 'main' and contains a tag with 'release' prefix
        //         allOf {
        //             branch 'main'
        //             tag 'release/*'
        //         }
        //     }
        //     steps {
        //         echo 'Deploying to Production environment...'
        //     }
        // }
    }
}

