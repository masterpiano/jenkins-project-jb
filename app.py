import boto3
import time
import os
import logging
from pythonjsonlogger import jsonlogger

# Connect to AWS
ec2 = boto3.client('ec2')

# Set logger for AWS instances
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(threadName) %(name) %(time) %(Running clusters) %(CLUSTER 1 IP) %(CLUSTER NAME) %(message) %(levelName)'
)
logHandler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logHandler.setLevel(logging.INFO)
logger.addHandler(logHandler)

# Print out instances details as json log
def log_instance_out(instance):
    instance_name = next(
        (tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed'
    )
    instance_dict = {
        "time": instance["LaunchTime"],
        "Running clusters": 1,
        "CLUSTER 1 IP": instance["PublicIpAddress"],
        "CLUSTER NAME": instance_name
    }
    logger.info("testing K8S REPORTING", extra=instance_dict)
def working_instances():
    # Use the client to get information about instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-code',
                'Values': ['16']
            }
            ,
            {
                'Name': 'tag:k8s.io/role/master',
                'Values': ['1']
            }
        ]
    )

    # Extract the instance information from the response
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)

    # Print the instance IDs and instance names
    for instance in instances:
        log_instance_out(instance)


repeat_time = int(os.environ.get('REPEAT_TIME_SECONDS',5))


while True:
    working_instances()
    time.sleep(repeat_time)
