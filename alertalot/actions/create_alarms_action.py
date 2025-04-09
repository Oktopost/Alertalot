import sys
import boto3

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.file_loader import load
from alertalot.generic.parameters import Parameters
from alertalot.generic.output import Output
from alertalot.validation.alarms_config_validator import AlarmsConfigValidator


def execute(run_args: ArgsObject, output: Output):
    """
    Create the alarms for an entity
    Currently supports only AWS/EC2 namespaced metrics
    
    Args:
        run_args (ArgsObject): CLI command line arguments
        output (Output): Output object to use
    """
    if run_args.params_file is None:
        raise ValueError("No parameters file provided")
    if run_args.ec2_id is None:
        raise ValueError("Target must be provided. Missing --instance-id argument.")

    parameters = Parameters()
    entity_object = run_args.get_aws_entity()

    parameters.update(Parameters.parse(run_args.params_file, run_args.region))

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

    for config in validator.parsed_config:

        cloudwatch_config = {
            "AlarmName": config["alarm-name"],
            "ComparisonOperator": config["comparison-operator"],
            "EvaluationPeriods": config["evaluation-periods"],
            "MetricName": config["metric-name"],
            "Namespace": "AWS/EC2",
            "Period": config["period"],
            "Statistic": config["statistic"],
            "Threshold": config["threshold"] * 100,
            "ActionsEnabled": False,
            "Dimensions": [{
                "Name": "InstanceId",
                "Value": run_args.ec2_id
            }]
        }

        if "alarm-actions" in config:
            cloudwatch_config["ActionsEnabled"] = True
            cloudwatch_config["AlarmActions"] = config["alarm-actions"]

        if "treat-missing-data" in config:
            cloudwatch_config["TreatMissingData"] = config["treat-missing-data"]

        if "unit" in config:
            cloudwatch_config["Unit"] = config["unit"]

        if "tags" in config:
            tags_dict = config.get("tags", {})
            cloudwatch_config["Tags"] = [{"Key": key, "Value": value} for key, value in tags_dict.items()]

        if run_args.is_verbose:
            output.print("Creating alarm:")
            output.print("---------")

            output.print_yaml(cloudwatch_config)

            output.print("---------")

        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_alarm(**cloudwatch_config)

        if run_args.is_verbose:
            output.print("Alarm Created")

