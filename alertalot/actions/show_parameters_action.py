from alertalot.actions.sub_actions.load_variables_file import LoadVariablesFile
from alertalot.generic.args_object import ArgsObject
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
    
    variables = LoadVariablesFile.execute(run_args, output)
    
    output.print_step(f"Variables:")
    output.print_key_value(variables)
