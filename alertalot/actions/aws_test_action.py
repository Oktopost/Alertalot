import sys
import boto3

from botocore.exceptions import ClientError

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputLevel


def execute(run_args: ArgsObject, output: Output):
    """
    Test if AWS is accessible from the current machine. Does not check permissions
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    output.print_step("Testing...")
    
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        
        if run_args.is_verbose:
            output.print_success(f"Access confirmed", OutputLevel.NORMAL)
            output.print_success(f"Account: {identity['Account']}, ARN: {identity['Arn']}")
    
    except ClientError as e:
        if run_args.is_verbose:
            output.print_failure(f"Failed to connect to AWS: {e}", OutputLevel.QUITE)
        
        sys.exit(1)
