import sys
import boto3

from botocore.exceptions import ClientError

from alertalot.generic.args_object import ArgsObject


def execute(run_args: ArgsObject):
    """
    Test if AWS is accessible from the current machine. Does not check permissions
    
    Args:
        run_args (ArgsObject): CLI command line arguments
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
