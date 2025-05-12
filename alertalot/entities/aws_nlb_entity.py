from typing import Any

from alertalot.generic.target_type import TargetType
from alertalot.entities.abstract_aws_lb_entity import AbstractAwsLbEntity


class AwsNlbEntity(AbstractAwsLbEntity):
    """
    Implementation of AbstractAwsLbEntity for AWS Network Load Balancer.
    
    This class provides NLB-specific functionality for validating CloudWatch alarm
    configurations and extracting resource values from NLB instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsNlbEntity instance.
        """
        super().__init__(entity_type=TargetType.NLB)
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/NetworkELB",
            "dimensions": {
                "LoadBalancer": "$LOAD_BALANCER_NAME"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "ActiveFlowCount",
            "ActiveFlowCount_TCP",
            "ConsumedLCUs",
            "ConsumedLCUs_TCP",
            "HealthyHostCount",
            "NewFlowCount",
            "NewFlowCount_TCP",
            "PeakBytesPerSecond",
            "PeakPacketsPerSecond",
            "PortAllocationErrorCount",
            "ProcessedBytes",
            "ProcessedBytes_TCP",
            "ProcessedPackets",
            "RejectedFlowCount",
            "TCP_Client_Reset_Count",
            "TCP_ELB_Reset_Count",
            "TCP_Target_Reset_Count",
            "UnHealthyHostCount",
            "UnhealthyRoutingFlowCount",
            "ZonalHealthStatus"
        ]
