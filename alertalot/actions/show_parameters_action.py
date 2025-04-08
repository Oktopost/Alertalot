from alertalot.generic.args_object import ArgsObject
from alertalot.generic.parameters import Parameters
from alertalot.generic.output import Output


def execute(run_args: ArgsObject, output: Output):
    """
    Load and print the parameters.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.params_file is None:
        raise ValueError("No parameters file provided")
    
    output.print_if_verbose(f"Config: {run_args.params_file}")
        
    if run_args.region is None:
        output.print("Region: <None>")
    else:
        output.print(f"Region: {run_args.region}")
        
    output.print_if_verbose()
    output.print_if_verbose("Config:")
    output.print_if_verbose("-------")
    
    config = Parameters.parse(run_args.params_file, run_args.region)
    
    output.print_parameters(config)
