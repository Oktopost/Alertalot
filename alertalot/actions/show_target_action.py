import boto3

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import get_aligned_dict
from alertalot.generic.output import Output


def execute(run_args: ArgsObject, output: Output):
    """
    Load the target from AWS and show the arguments for this instance.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.ec2_id is None:
        raise ValueError("Target must be provided. Missing --instance-id argument.")
    
    entity_object = run_args.get_aws_entity()
    
    if run_args.is_verbose:
        print(f"Loading instance {run_args.ec2_id}...")
    
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    import time
    from rich.live import Live
    from rich.spinner import Spinner
    spinner = Spinner('bouncingBall')

    console = Console()
    with Live(spinner, console=console, transient=True):
        instance = entity_object.load_entity(run_args.ec2_id)
    
    # instance = entity_object.load_entity(run_args.ec2_id)
    
    if run_args.is_verbose:
        print("Instance found")
        print()
    
    values = entity_object.get_resource_values(instance)
    print(get_aligned_dict(values, padding=4))
