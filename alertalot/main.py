import sys
import argparse

from alertalot.generic.args_object import ArgsObject

from alertalot.actions import show_parameters_action
from alertalot.actions import show_alarms_template_action
from alertalot.actions import show_target_action
from alertalot.actions import aws_test_action
from alertalot.generic.output import Output


def __parse_args() -> ArgsObject:
    """
    Parse command line arguments for the application.
    
    Returns:
        argparse.Namespace: An object containing all parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create Cloudwatch alerts for "
                    "AWS resources based on predefined config")
    
    parser.add_argument("--ec2-id", type=str, help="ID of an EC2 instance to generate the alerts for")
    parser.add_argument("--params-file", type=str, help="Relative path to the parameters file to use")
    parser.add_argument("--template-file", type=str, help="Relative path to the template file to use")
    
    parser.add_argument(
        "--region",
        type=str,
        help="The AWS region to use",
        default="us-east-1")
    
    parser.add_argument(
        "--dry-run",
        type=bool,
        help="Simulate the requests without executing them",
        default=False)
    
    ##########
    # Output #
    ##########
    output_group = parser.add_mutually_exclusive_group()
    
    output_group.add_argument(
        "-q", "--quiet",
        action="store_true",
        dest="quiet",
        help="Suppress all non-error output")
    
    output_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="Enable verbose output to show details about executed actions")
    
    ###########
    # Actions #
    ###########
    actions_group = parser.add_mutually_exclusive_group()
    
    actions_group.add_argument(
        "--test-aws",
        action="store_true",
        help="If passed, only check if AWS is accessible by calling sts:GetCallerIdentity. "
             "This does not check any other permissions. Run with --verbose if you want output.",
        default=False)
    
    actions_group.add_argument(
        "--show-parameters", "--show-params",
        action="store_true",
        help="If specified, only loads the parameters.yaml file and outputs the result. "
             "If a region is provided, parameters defined for that region will be merged "
             "with those in the global list.",
        default=False)
    
    actions_group.add_argument(
        "--show-instance",
        action="store_true",
        help="If set, load and describe the target object. A valid target must be provided.",
        default=False)
    
    actions_group.add_argument(
        "--show-template",
        action="store_true",
        help="If specified, only loads the alarms template file, performance validations, and outputs the result. "
             "If a region or aws resource are provided, parameters defined for that region and aws resource"
             "with those in the global list.",
        default=False)
    
    return ArgsObject(parser.parse_args())


def __execute(args_object: ArgsObject, output: Output) -> None:
    if args_object.show_parameters:
        show_parameters_action.execute(args_object, output)
    elif args_object.test_aws:
        aws_test_action.execute(args_object, output)
    elif args_object.show_instance:
        show_target_action.execute(args_object, output)
    elif args_object.show_template:
        show_alarms_template_action.execute(args_object, output)


if __name__ == "__main__":
    args_object = __parse_args()
    
    output = Output(
        is_quiet=args_object.is_quiet,
        is_verbose=args_object.is_verbose
    )
    
    try:
        __execute(args_object, output)
    except Exception as exception:
        output.print_error(exception)
        raise exception
        sys.exit(1)
