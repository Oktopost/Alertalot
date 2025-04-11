import sys
import argparse


from alertalot.actions import show_variables_action
from alertalot.actions import show_alarms_template_action
from alertalot.actions import create_alarms_action
from alertalot.actions import show_target_action
from alertalot.actions import aws_test_action
from alertalot.generic.output import Output
from alertalot.generic.args_object import ArgsObject
from alertalot.exception.invalid_template_exception import InvalidTemplateException
from alertalot.generic.output import OutputLevel


def __parse_key_value(argument: str) -> (str, str):
    """
    Parse a string in the format 'key=value' into separate key and value strings.
    
    Args:
        argument: A string in the format 'key=value' to be parsed.

    Returns:
        A tuple containing two strings: (key, value)
    """
    try:
        key, value = argument.split('=', 1)
        return key, value
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"'{argument}' is not a valid key=value pair") from e


def __create_args_object() -> argparse.ArgumentParser:
    """
    Parse command line arguments for the application.
    
    Returns:
        argparse.Namespace: An object containing all parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create Cloudwatch alerts for "
                    "AWS resources based on predefined config")
    
    parser.add_argument("--ec2-id", type=str, help="ID of an EC2 instance to generate the alerts for")
    
    parser.add_argument(
        "--vars-file", "--variables-file",
        type=str,
        help="Relative path to the variables file to use")
    
    parser.add_argument(
        "--var",
        action="append",
        type=__parse_key_value,
        dest="variables",
        default=[],
        help="Key/value pairs to use for variables"
    )
    
    parser.add_argument("--template-file", type=str, help="Relative path to the template file to use")
    
    parser.add_argument(
        "--region",
        type=str,
        help="The AWS region to use",
        default="us-east-1")
    
    parser.add_argument(
        "--trace",
        action="store_true",
        dest="trace",
        help="If set, when printing out an exception also add a pretty print of the stack trace. "
             "Otherwise only the error message is printed.")
    
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
    actions_group = parser.add_mutually_exclusive_group(required=True)
    
    actions_group.add_argument(
        "--create-alarms", "--create", "-c",
        action="store_true",
        help="If specified, loads the alarms template file, performance validations, and creates alarms for it. "
             "If a region or aws resource are provided, variables defined for that region and aws resource"
             "with those in the global list.",
        default=False)
    
    actions_group.add_argument(
        "--show-variables", "--show-vars",
        action="store_true",
        help="If specified, only loads the variables.yaml file and outputs the result. "
             "If a region is provided, variables defined for that region will be merged "
             "with those in the global list.",
        default=False)
    
    actions_group.add_argument(
        "--show-target",
        action="store_true",
        help="If set, load and describe the target object. A valid target must be provided.",
        default=False)
    
    actions_group.add_argument(
        "--show-template",
        action="store_true",
        help="If specified, only loads the alarms template file, performance validations, and outputs the result. "
             "If a region or aws resource are provided, variables defined for that region and aws resource"
             "with those in the global list.",
        default=False)
    
    actions_group.add_argument(
        "--test-aws",
        action="store_true",
        help="If passed, only check if AWS is accessible by calling sts:GetCallerIdentity. "
             "This does not check any other permissions. Run with --verbose if you want output.",
        default=False)
    
    return parser
    

def __parse_args() -> ArgsObject:
    """
    Parse command line arguments for the application.
    
    Returns:
        ArgsObject: An object containing all parsed command-line arguments.
    """
    args_parser = __create_args_object()
    args_array = args_parser.parse_args()
    
    return ArgsObject(args_array)


def __execute(args_object: ArgsObject, output: Output) -> None:
    """
    Execute the target action based on the provided arguments.
    
    Args:
        args_object (ArgsObject): An object containing all parsed command-line arguments.
        output (Output): The output object to use.
    """
    if args_object.show_variables:
        show_variables_action.execute(args_object, output)
    elif args_object.test_aws:
        aws_test_action.execute(args_object, output)
    elif args_object.show_target:
        show_target_action.execute(args_object, output)
    elif args_object.show_template:
        show_alarms_template_action.execute(args_object, output)
    elif args_object.create_alarms:
        create_alarms_action.execute(args_object, output)
    else:
        output.print_failure("It seems like no action was selected", level=OutputLevel.QUITE)
        __create_args_object().print_help()
        sys.exit(1)


if __name__ == "__main__":
    args_obj = __parse_args()
    
    out = Output(
        is_quiet=args_obj.is_quiet,
        is_verbose=args_obj.is_verbose,
        with_trace=args_obj.with_trace
    )
    
    try:
        __execute(args_obj, out)
    except InvalidTemplateException as e:
        out.print_line(color="red")
        out.print_failure("Errors encountered while parsing the template file", level=OutputLevel.QUITE)
        out.print_list("▷  ", "red", e.issues, level=OutputLevel.QUITE)
        out.print_line(color="red")
        sys.exit(1)
    except Exception as exception: # pylint: disable=W0718
        out.print_error(exception, level=OutputLevel.QUITE)
        sys.exit(1)
