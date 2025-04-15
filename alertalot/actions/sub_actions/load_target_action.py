from typing import Any

from alertalot.generic.output import Output
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.variables import Variables
from alertalot.entities.aws_entity_factory import AwsEntityFactory


class LoadTargetAction:
    """
    Action responsible for loading a target from AWS based on the passed resource
    type/ID.
    """
    @staticmethod
    def execute(run_args: ArgsObject, output: Output, variables: Variables|None = None) -> dict[str, Any]:
        """
        Load the target instance by its ID
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
            variables (Variables | None): Variables object to update, if passed.
        """
        entity_object = AwsEntityFactory.from_args(run_args)
        
        if entity_object is None:
            raise ValueError("Target must be provided. Missing id argument.")
        
        output.print_step(f"Loading instance {run_args.ec2_id}...")
        data = output.spinner(lambda: entity_object.load_entity(run_args.ec2_id))
        
        if variables is not None:
            variables.update(entity_object.get_resource_values(data))
        
        return data
