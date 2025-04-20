import os

from alertalot.generic.output import Output
from alertalot.generic.variables import Variables
from alertalot.generic.args_object import ArgsObject


class LoadVariableFilesAction:
    """
    Action responsible for loading the variables file.
    """
    @staticmethod
    def execute(run_args: ArgsObject, output: Output) -> Variables:
        """
        Load all the variable files.
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
        """
        if not run_args.var_files:
            raise ValueError("No variable files provided")
        
        output.print_step("Loading variable files...")
        output.print_key_value({
            "Region": run_args.region,
            "Variable Files": os.linesep.join(run_args.var_files),
        })
        
        data = Variables.parse(run_args.var_files, run_args.region)
        data.update(run_args.variables)
        
        output.print_success("Files loaded")
        
        return data
