pipeline {
  agent any
  parameters {
        string(name: 'AWS_DEFAULT_REGION', defaultValue: 'us-east-1', description: 'The region of the AWS')
        string(name: 'REPEAT_TIME_SECONDS', defaultValue: '300', description: 'Period of time to check the working AWS instnces')
  }

  environment {
        AWS_ACCESS_KEY_ID = credentials('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('aws_secret_access_key')
  }

	
  
	stages {

		stage('Build docker') {

			steps {
                script{
                    sh "git merge --no-ff dev"
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_REPO')]) {
                        def imageName = "${DOCKER_REPO}/k8stest:${env.BUILD_NUMBER}"
                        def builtImage = docker.build($imageName)
                    }
                    // sh "docker build -t k8stest:${env.BUILD_NUMBER} ./"
                }
			}
		}

		stage('Test') {
			steps {
				sh "docker run -td --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --env AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} --env REPEAT_TIME_SECONDS=${REPEAT_TIME_SECONDS} --name test-container-${env.BUILD_NUMBER} $imageName"
				script{

					sleep time: 5, unit: 'SECONDS'
				    def containerStatus = sh(script: "docker inspect -f '{{.State.Status}}' test-container-${env.BUILD_NUMBER}", returnStdout: true).trim()
				    echo "Container state: ${containerStatus}"

			        sh "docker logs test-container-${env.BUILD_NUMBER}"
		            	
					if (containerStatus != "running") {					
				        	error "An error occured on the last attempt to run the container of image working-ec2"
					}
				}
			}
		}
		
		stage('Deploy') {
			steps {
				script{
					docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials') {
						//sh "docker tag k8stest:${env.BUILD_NUMBER} bjrus27/k8stest:${env.BUILD_NUMBER}"
						builtImage.push()
					}
				}
			}	
		}

        stage('Merge Git') {
			steps {
				sh "git push"
                echo 'The pipeline worked succesfully'
			}	
		}
	}
	post { 
		always { 
	            cleanWs()
	        }
	}	
}