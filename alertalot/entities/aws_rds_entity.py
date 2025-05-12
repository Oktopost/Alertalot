from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsRdsEntity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS RDS instances.
    
    This class provides RDS-specific functionality for loading database instance data,
    validating CloudWatch alarm configurations, and extracting resource values
    from RDS instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsRdsEntity instance.
        """
        super().__init__(entity_type=TargetType.RDS)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        rds = boto3.client("rds")
        response = rds.describe_db_instances(DBInstanceIdentifier=entity_id)
        
        try:
            return response["DBInstances"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected RDS instance data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "DBInstanceIdentifier" not in resource:
            raise ValueError("Missing DBInstanceIdentifier property for RDS instance")
        
        result = {
            "DB_INSTANCE_ID": resource["DBInstanceIdentifier"],
        }
        
        if "DBInstanceArn" in resource:
            result["DB_INSTANCE_ARN"] = resource["DBInstanceArn"]
            
        if "DBInstanceClass" in resource:
            result["DB_INSTANCE_CLASS"] = resource["DBInstanceClass"]
            
        if "Engine" in resource:
            result["DB_ENGINE"] = resource["Engine"]
            
        if "TagList" in resource:
            for tag in resource['TagList']:
                if 'Key' not in tag or 'Value' not in tag:
                    continue
                
                if tag["Key"] == 'Name':
                    result["DB_INSTANCE_NAME"] = tag["Value"]
                    break
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/RDS",
            "dimensions":
            {
                "DBInstanceIdentifier": "$DB_INSTANCE_ID"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "BinLogDiskUsage",
            "BurstBalance",
            "CPUUtilization",
            "CPUCreditUsage",
            "CPUCreditBalance",
            "DatabaseConnections",
            "DiskQueueDepth",
            "FailedSQLServerAgentJobsCount",
            "FreeableMemory",
            "FreeStorageSpace",
            "MaximumUsedTransactionIDs",
            "NetworkReceiveThroughput",
            "NetworkTransmitThroughput",
            "OldestReplicationSlotLag",
            "ReadIOPS",
            "ReadLatency",
            "ReadThroughput",
            "ReplicaLag",
            "ReplicationSlotDiskUsage",
            "SwapUsage",
            "TransactionLogsDiskUsage",
            "TransactionLogsGeneration",
            "WriteIOPS",
            "WriteLatency",
            "WriteThroughput"
        ]
