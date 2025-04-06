import boto3

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import get_aligned_dict


def execute(run_args: ArgsObject):
    """
    Load the target from AWS and show the arguments for this instance.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
    """
    if run_args.instance_id is None:
        raise ValueError("Target must be provided. Missing --instance-id argument.")
    
    if run_args.is_verbose:
        print(f"Loading instance {run_args.instance_id}...")
    
    instance_id = run_args.instance_id
    entity_object = run_args.get_aws_entity()
    
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances(InstanceIds=[instance_id])
    
    if run_args.is_verbose:
        print("Instance found")
        print()
    
    values = entity_object.get_resource_values(response)
    print(get_aligned_dict(values, padding=4))
