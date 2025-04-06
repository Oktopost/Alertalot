from alertalot.generic.args_object import ArgsObject
from alertalot.generic.parameters import Parameters


def execute(run_args: ArgsObject):
    """
    Load and print the parameters.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
    """
    if run_args.params_file is None:
        raise ValueError("No parameters file provided")
    
    if run_args.is_verbose:
        print(f"Config: {run_args.params_file}")
        
        if run_args.region is None:
            print("Region: <None>")
        else:
            print(f"Region: {run_args.region}")
        
        print()
        print("Config:")
        print("-------")
    
    config = Parameters.parse(run_args.params_file, run_args.region)
    
    print(config.as_string())
