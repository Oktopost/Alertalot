from typing import Any

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsGenericEntity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for a non-specific entity type.
    """
    def __init__(self):
        super().__init__(entity_type=TargetType.GENERIC)
    
    
    def _supported_metrics(self) -> list[str]:
        return []
    
    
    def get_additional_config(self) -> dict[str, Any]:
        return {}
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        raise NotImplementedError("Invalid operation for a generic alarm type")
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        raise NotImplementedError("Invalid operation for a generic alarm type")
