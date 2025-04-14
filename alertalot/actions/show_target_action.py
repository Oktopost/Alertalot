from alertalot.actions.sub_actions.load_target_action import LoadTargetAction
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputLevel
from alertalot.entities.aws_entity_factory import AwsEntityFactory


def execute(run_args: ArgsObject, output: Output):
    """
    Load the target from AWS and show the arguments for this instance.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    entity_object = AwsEntityFactory.from_args(run_args)
    
    if entity_object is None:
        raise ValueError("Target must be provided. Missing id argument.")
    
    target = LoadTargetAction.execute(run_args, output)
    
    output.print_step(f"Variables for instance {run_args.ec2_id}:")
    output.print_key_value(entity_object.get_resource_values(target), level=OutputLevel.NORMAL)
