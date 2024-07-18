import boto3
import logging

# Setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the connection
ec2 = boto3.resource('ec2', region_name='eu-west-3')

def lambda_handler(event, context):
    # All stopped EC2 instances.
    filters = [{
            'Name': 'tag:AutoStart',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    # Filter the instances
    instances = ec2.instances.filter(Filters=filters)

    # Locate all stopped instances
    RunningInstances = [instance.id for instance in instances]
    
    if len(RunningInstances) > 0:
        # Perform the startup
        AutoStarting = ec2.instances.filter(InstanceIds=RunningInstances).start()
        print(AutoStarting)
    else:
        print("Nothing to see here")

