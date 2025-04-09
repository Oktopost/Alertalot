from alertalot.generic.args_object import ArgsObject
from alertalot.generic.parameters import Parameters
from alertalot.generic.output import Output


class LoadVariablesFileAction:
    @staticmethod
    def execute(run_args: ArgsObject, output: Output) -> Parameters:
        """
        Load the variables file.
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
        """
        if run_args.params_file is None:
            raise ValueError("No variables file provided")
        
        output.print_step("Loading variables file...")
        
        if output.is_verbose:
            output.print_key_value({
                "Region": run_args.region,
                "Variables File": run_args.params_file,
            })
        
        data = Parameters.parse(run_args.params_file, run_args.region)
        
        output.print_success("File loaded")
        
        return data
