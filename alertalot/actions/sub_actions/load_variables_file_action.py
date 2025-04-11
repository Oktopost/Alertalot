from alertalot.generic.args_object import ArgsObject
from alertalot.generic.variables import Variables
from alertalot.generic.output import Output


class LoadVariablesFileAction:
    """
    Action responsible for loading the variables file.
    """
    @staticmethod
    def execute(run_args: ArgsObject, output: Output) -> Variables:
        """
        Load the variables file.
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
        """
        if run_args.vars_file is None:
            raise ValueError("No variables file provided")
        
        output.print_step("Loading variables file...")
        output.print_key_value({
            "Region": run_args.region,
            "Variables File": run_args.vars_file,
        })
        
        data = Variables.parse(run_args.vars_file, run_args.region)
        data.update(run_args.variables)
        
        output.print_success("File loaded")
        
        return data
