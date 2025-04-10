from typing import Any

import boto3

from alertalot.generic.output import Output, OutputLevel


class CreateAlarmAction:
    """
    Action responsible for creating a single alarm.
    """
    
    @staticmethod
    def execute(
            output: Output,
            config: dict[str, Any],
            entity_id: str
    ) -> None:
        """
        Create a single Alarm for an entity
        
        Args:
            output (Output): Output object to use
            config (dict[str, Any]): The alarm's configuration
            entity_id (str): The target entity ID
        """
        cloudwatch = boto3.client('cloudwatch')
        name = config["alarm-name"]
        
        output.print_step(f"Creating alarm \"{name}\"...")
        
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
                "Value": entity_id
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
        
        output.print_bullet("Alarm configuration:", level=OutputLevel.VERBOSE)
        output.print_yaml(cloudwatch_config, level=OutputLevel.VERBOSE)
        
        output.spinner(lambda: cloudwatch.put_metric_alarm(**cloudwatch_config))
        output.print_success("Alarm Created")
