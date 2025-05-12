from typing import Any

from alertalot.generic.target_type import TargetType
from alertalot.entities.abstract_aws_lb_entity import AbstractAwsLbEntity


class AwsAlbEntity(AbstractAwsLbEntity):
    """
    Implementation of AbstractAwsLbEntity for AWS Application Load Balancer.
    
    This class provides ALB-specific functionality for validating CloudWatch alarm
    configurations and extracting resource values from ALB instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsAlbEntity instance.
        """
        super().__init__(entity_type=TargetType.ALB)
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/ApplicationELB",
            "dimensions": {
                "LoadBalancer": "$LOAD_BALANCER_NAME"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "RequestCount",
            "TargetResponseTime",
            "HTTPCode_Target_2XX_Count",
            "HTTPCode_Target_3XX_Count",
            "HTTPCode_Target_4XX_Count",
            "HTTPCode_Target_5XX_Count",
            "HTTPCode_ELB_3XX_Count",
            "HTTPCode_ELB_4XX_Count",
            "HTTPCode_ELB_5XX_Count",
            "HTTPCode_ELB_502_Count",
            "HTTPCode_ELB_503_Count",
            "HTTPCode_ELB_504_Count",
            "HealthyHostCount",
            "UnHealthyHostCount",
            "TargetConnectionErrorCount",
            "ELBConnectionErrorCount",
            "ClientTLSNegotiationErrorCount",
            "TargetTLSNegotiationErrorCount",
            "RejectedConnectionCount",
            "NewConnectionCount",
            "ActiveConnectionCount",
            "ProcessedBytes",
            "ConsumedLCUs",
            "AnomalousHostCount",
            "DesyncMitigationMode_NonCompliant_Request_Count",
            "ExcessiveLowReputationPackets",
            "ForwardedInvalidHeaderRequestCount",
            "HealthyStateDNS",
            "HealthyStateRouting",
            "HTTP_Redirect_Count",
            "MitigatedHostCount",
            "PeakLCUs",
            "RequestCountPerTarget",
            "RuleEvaluations",
            "UnhealthyRoutingRequestCount",
            "UnhealthyStateDNS",
            "UnhealthyStateRouting"
        ]
