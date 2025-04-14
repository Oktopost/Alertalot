from alertalot.generic.output import Output
from alertalot.generic.variables import Variables
from alertalot.generic.file_loader import load
from alertalot.generic.args_object import ArgsObject
from alertalot.entities.aws_entity_factory import AwsEntityFactory
from alertalot.exception.invalid_template_exception import InvalidTemplateException
from alertalot.validation.alarms_config_validator import AlarmsConfigValidator


class LoadTemplateAction:
    """
    Action responsible for loading a template and validating it.
    """
    @staticmethod
    def execute(
            run_args: ArgsObject,
            output: Output,
            variables: Variables,
            *,
            is_strict: bool = True) -> AlarmsConfigValidator:
        """
        Load and validate the alarms template file.
        
        Args:
            run_args (ArgsObject): CLI command line arguments
            output (Output): Output object to use
            variables (Variables): Parameters to use for substitution
            is_strict (bool): If True, failed the execution if template is invalid
        """
        if run_args.vars_file is None:
            raise ValueError("No variables file provided")
        
        output.print_step(f"Loading template file {run_args.template_file}...")
        output.print_bullet("Using Variables:")
        output.print_key_value(variables)
        
        alarm_config = load(run_args.template_file)
    
        validator = AlarmsConfigValidator(
            AwsEntityFactory.from_args(run_args),
            variables,
            alarm_config,
        )
        
        if validator.validate(is_strict):
            output.print_success("File loaded")
            return validator
        else:
            raise InvalidTemplateException(run_args.template_file, validator.issues)
