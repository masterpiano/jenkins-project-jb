# jenkins-project-jb
Before you run the pipeline, set the following credentials and parameters:

Parameters:
  AWS_DEFAULT_REGION - an AWS region your EC2 instances are running on
  REPEAT_TIME_SECONDS - the ammount of time in seconds the Python code will check the working EC2 instances

Credentials:
  aws_access_key_id  - an AWS Access key. Generate it from your AWS account
  aws_secret_access_key  - comes with AWS Access key
  docker-credentials - a credentials to your dockerhub account. Generate tokens in your account for that metter
  github-credentials - the credentials to your github account. Again, generate tokens.
  
