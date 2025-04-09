from alertalot.actions.sub_actions.load_target_action import LoadTargetAction
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputLevel


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
    target = LoadTargetAction.execute(run_args, output)
    
    output.print_step(f"Variables for instance {run_args.ec2_id}:")
    output.print_key_value(entity_object.get_resource_values(target), level=OutputLevel.NORMAL)

