from alertalot.generic.output import Output, OutputLevel
from alertalot.generic.parameters import Parameters
from alertalot.generic.file_loader import load
from alertalot.generic.args_object import ArgsObject
from alertalot.exception.invalid_template_exception import InvalidTemplateException
from alertalot.validation.alarms_config_validator import AlarmsConfigValidator


class LoadTemplateAction:
    @staticmethod
    def execute(run_args: ArgsObject, output: Output, parameters: Parameters) -> AlarmsConfigValidator:
        """
        Load the variables file.
        
        Args:
            run_args (ArgsObject): CLI command line arguments.
            output (Output): Output object to use.
            parameters (Parameters): Parameters to use for substitution.
        """
        if run_args.params_file is None:
            raise ValueError("No variables file provided")
        
        output.print_step(f"Loading template file {run_args.template_file}...")
        output.print_bullet("Using Variables:")
        output.print_key_value(parameters)
        
        alarm_config = load(run_args.template_file)
    
        validator = AlarmsConfigValidator(
            run_args.get_aws_entity(),
            parameters,
            alarm_config
        )
        
        if validator.validate():
            output.print_success("File loaded")
            return validator
        else:
            raise InvalidTemplateException(run_args.template_file, validator.issues)
