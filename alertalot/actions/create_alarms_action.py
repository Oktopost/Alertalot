import time

from alertalot.actions.sub_actions.create_alarm_action import CreateAlarmAction
from alertalot.actions.sub_actions.load_target_action import LoadTargetAction
from alertalot.actions.sub_actions.load_template_action import LoadTemplateAction
from alertalot.actions.sub_actions.load_variables_file_action import LoadVariablesFileAction
from alertalot.generic.output import Output, OutputLevel
from alertalot.generic.args_object import ArgsObject


def execute(run_args: ArgsObject, output: Output):
    """
    Create the alarms for an entity.
    
    Currently, supports only AWS/EC2 namespaced metrics
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.vars_file is None:
        raise ValueError("No parameters file provided")
    if run_args.ec2_id is None:
        raise ValueError("Target must be provided. Missing --ec2-id argument.")

    # 1. Load variables file
    variables = LoadVariablesFileAction.execute(run_args, output)
    
    # 2. Load the target object
    LoadTargetAction.execute(run_args, output, variables)
    
    # 3. Load and validate alarms config
    validator = LoadTemplateAction.execute(run_args, output, variables)
    
    # 4. Create the alarms.
    start_time = time.time()
    
    for config in validator.parsed_config:
        CreateAlarmAction.execute(output, config, run_args.ec2_id)
    
    runtime = time.time() - start_time
    
    # 5. Output success
    output.print_step("All alarms created")
    output.print_bullet(f"Total {len(validator.parsed_config)} alarms created", level=OutputLevel.NORMAL)
    output.print_bullet(f"In {runtime:.2f} seconds")
