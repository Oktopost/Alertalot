from typing import Any

from alertalot.generic.output import Output
from alertalot.generic.args_object import ArgsObject


class LoadTarget:
    @staticmethod
    def execute(run_args: ArgsObject, output: Output) -> dict[str, Any]:
        """
        Load the target instance by its ID
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
        """
        entity_object = run_args.get_aws_entity()
        
        output.print_step(f"Loading instance {run_args.ec2_id}...")
        return output.spinner(lambda: entity_object.load_entity(run_args.ec2_id))
