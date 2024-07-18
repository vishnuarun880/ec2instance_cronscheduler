import boto3
import logging

# Setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the connection and set the region
ec2 = boto3.resource('ec2', region_name='eu-west-3')

def lambda_handler(event, context):
    # All running EC2 instances.
    filters = [{
            'Name': 'tag:AutoStop',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    # Filter the instances which are stopped
    instances = ec2.instances.filter(Filters=filters)

    # Locate all running instances
    RunningInstances = [instance.id for instance in instances]
    
    if len(RunningInstances) > 0:
        # Perform the shutdown
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print(shuttingDown)
    else:
        print("Nothing to see here")
