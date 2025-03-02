import boto3

from alertalot.generic.args_object import ArgsObject


def execute(run_args: ArgsObject):
    """
    Load the target from AWS and show the arguments for this instance.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
    """
    if run_args.instance_id is None:
        raise ValueError("Target must be provided. Missing --instance-id argument.")
    
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances(InstanceIds=[run_args.instance_id])
    
    instance = response["Reservations"][0]["Instances"][0]
    
    instance_id = instance['InstanceId']
    name = None
    
    for tag in instance['Tags']:
        if tag["Key"] == 'Name':
            name = tag["Value"]
            break
    
    print(f"$INSTANCE_ID   : {instance_id}")
    print(f"$INSTANCE_NAME : {name}")
        