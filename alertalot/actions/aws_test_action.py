import sys
import boto3

from botocore.exceptions import ClientError

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output


def execute(run_args: ArgsObject, output: Output):
    """
    Test if AWS is accessible from the current machine. Does not check permissions
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        
        if run_args.is_verbose:
            print(f"Access confirmed.")
            print(f"Account: {identity['Account']}, ARN: {identity['Arn']}")
    
    except ClientError as e:
        if run_args.is_verbose:
            print(f"Access denied: {e}")
        
        sys.exit(1)
