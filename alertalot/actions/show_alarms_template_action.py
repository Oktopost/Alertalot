import sys

from alertalot.generic.parameters import Parameters
from alertalot.generic.args_object import ArgsObject
from alertalot.generic.file_loader import load
from alertalot.validation.alarms_config_validator import AlarmsConfigValidator
from alertalot.generic.output import Output


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
        parameters.update(Parameters.parse(run_args.params_file, run_args.region))
    
    if run_args.ec2_id is not None:
        output.print_if_verbose(f"Loading instance {run_args.ec2_id}...")
        parameters.update(entity_object.load_resource_values(run_args.ec2_id))
        output.print_if_verbose()
    
    alarm_config = load(run_args.template_file)
    
    validator = AlarmsConfigValidator(
        entity_object,
        parameters,
        alarm_config
    )
    
    if not validator.validate():
        print("Issues found in the alarms config:")
        print("---------")
        print("\n".join(validator.issues))
        print("---------")
        
        sys.exit(1)
    elif run_args.is_verbose:
        output.print(f"Total alarms found: {len(validator.parsed_config)}")
        output.print("Template")
        output.print("---------")
        
        output.print_yaml(validator.parsed_config)
        
        output.print("---------")
        
