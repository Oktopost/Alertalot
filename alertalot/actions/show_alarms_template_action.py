import sys

from alertalot.actions.sub_actions.load_target import LoadTarget
from alertalot.actions.sub_actions.load_template import LoadTemplate
from alertalot.actions.sub_actions.load_variables_file import LoadVariablesFile
from alertalot.generic.parameters import Parameters
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.output import Output, OutputType
from alertalot.exception.action_failed_exception import ActionFailedException


def execute(run_args: ArgsObject, output: Output):
    """
    Load and print the alarms configuration file.
    
    If AWS Resource ID is provided, any $VARIABLE in the config string will be replaced with
    corresponding values from this resource
    
    If the parameters config file is provided, any $VARIABLE in the config string will be replaced with
    corresponding values from the parameters file.
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    parameters = Parameters()
    entity_object = run_args.get_aws_entity()
    
    if entity_object is None:
        raise ValueError("Either entity type must be specified, or entity ID must be provided")
    
    if run_args.template_file is None:
        raise ValueError("No template file provided. Missing the --template-file argument.")
    
    if run_args.params_file:
        parameters.update(LoadVariablesFile.execute(run_args, output))
    
    if run_args.ec2_id is not None:
        target = LoadTarget.execute(run_args, output)
        values = entity_object.get_resource_values(target)
        
        parameters.update(values)
    
    validator = LoadTemplate.execute(run_args, output, parameters)
    
    if validator is None:
        raise ActionFailedException()
    
    output.print_line()
    output.print_yaml(validator.parsed_config, type=OutputType.ALWAYS)
    