import boto3

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.parameters import Parameters
from alertalot.generic.output import Output


def execute(run_args: ArgsObject, output: Output):
    """
    Create the alarms for an entity
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.params_file is None:
        raise ValueError("No parameters file provided")
    if run_args.ec2_id is None:
        raise ValueError("Target must be provided. Missing --instance-id argument.")
    
    if run_args.is_verbose:
        region_id = run_args.region or "<None>"
        
        # get_aligned_dict({
        #     "Instance ID": run_args.instance_id,
        #     "Config File": run_args.params_file,
        #     "Region": region_id,
        # })
        
    config = Parameters.parse(run_args.params_file, run_args.region)
    
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances(InstanceIds=[run_args.ec2_id])

