import argparse

from alertalot.generic.args_object import ArgsObject
from alertalot.actions import show_parameters_action
from alertalot.actions import aws_test_action
from alertalot.actions import show_target_action


def parse_args() -> ArgsObject:
    """
    Parse command line arguments for the application.
    
    Returns:
        argparse.Namespace: An object containing all parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create Cloudwatch alerts for "
                    "AWS resources based on predefined config")
    
    parser.add_argument("--instance-id", type=str, help="ID of an EC2 instance to generate the alerts for")
    parser.add_argument("--params-file", type=str, help="Relative path to the parameters file to use")
    parser.add_argument("--template-file", type=str, help="Relative path to the template file to use")
    
    parser.add_argument("--region", type=str, help="The AWS region to use")
    
    parser.add_argument(
        "--dry-run",
        type=bool,
        help="Simulate the requests without executing them",
        default=False)
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="Enable verbose output to show details about executed actions")
    
    ###########
    # Actions #
    ###########
    parser.add_argument(
        "--show-parameters", "--show-params",
        action="store_true",
        help="If specified, only loads the parameters.yaml file and outputs the result. "
             "If a region is provided, parameters defined for that region will be merged "
             "with those in the global list.",
        default=False)
    
    parser.add_argument(
        "--test-aws",
        action="store_true",
        help="If passed, only check if AWS is accessible by calling sts:GetCallerIdentity. "
             "This does not check any other permissions. Run with --verbose if you want output.",
        default=False)
    
    parser.add_argument(
        "--show-instance",
        action="store_true",
        help="If set, load and describe the target object. A valid target must be provided.",
        default=False)
    
    return ArgsObject(parser.parse_args())


if __name__ == "__main__":
    args_object = parse_args()
    
    if args_object.show_parameters:
        show_parameters_action.execute(args_object)
    elif args_object.test_aws:
        aws_test_action.execute(args_object)
    elif args_object.show_instance:
        show_target_action.execute(args_object)
