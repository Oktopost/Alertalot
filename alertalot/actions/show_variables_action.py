from alertalot.actions.sub_actions.load_variables_file_action import LoadVariablesFileAction
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputLevel


def execute(run_args: ArgsObject, output: Output):
    """
    Load and print the variables file.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.vars_file is None:
        raise ValueError("No variables file provided")
    
    variables = LoadVariablesFileAction.execute(run_args, output)
    
    output.print_step(f"Variables:")
    output.print_key_value(variables, level=OutputLevel.NORMAL)
