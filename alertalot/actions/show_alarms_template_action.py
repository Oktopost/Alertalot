from alertalot.actions.sub_actions.load_target_action import LoadTargetAction
from alertalot.actions.sub_actions.load_template_action import LoadTemplateAction
from alertalot.actions.sub_actions.load_variables_file_action import LoadVariablesFileAction
from alertalot.generic.variables import Variables
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputLevel


def execute(run_args: ArgsObject, output: Output):
    """
    Load and print the alarms configuration file.
    
    If AWS Resource ID is provided, any $VARIABLE in the config string will be replaced with
    corresponding values from this resource
    
    If the variables config file is provided, any $VARIABLE in the config string will be replaced with
    corresponding values from the variables file.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    variables = Variables()
    entity_object = run_args.get_aws_entity()
    
    if entity_object is None:
        raise ValueError("Either entity type must be specified, or entity ID must be provided")
    
    if run_args.template_file is None:
        raise ValueError("No template file provided. Missing the --template-file argument.")
    
    if run_args.vars_file:
        variables.update(LoadVariablesFileAction.execute(run_args, output))
    
    if run_args.ec2_id is not None:
        target = LoadTargetAction.execute(run_args, output)
        values = entity_object.get_resource_values(target)
        
        variables.update(values)
    
    validator = LoadTemplateAction.execute(run_args, output, variables, is_strict=run_args.is_strict)
    
    output.print_line()
    output.print_yaml(validator.parsed_config, level=OutputLevel.NORMAL)
    