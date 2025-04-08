from abc import ABC, abstractmethod

from alertalot.validation.aws_alarm_validator import AwsAlarmValidator


class BaseAwsEntity(ABC):
    """
    Base abstract class for AWS entities that can be monitored with CloudWatch alarms.
    
    This class defines the interface that all AWS entity implementations must adhere to,
    including methods for loading entity data, validating alarm configurations, and
    extracting resource values for alarm creation.
    """
    
    
    @abstractmethod
    def load_entity(self, id: str) -> dict[str, any]:
        """
        Load entity data from AWS based on the provided identifier.
        
        Args:
            id (str): The identifier of the entity to load
            
        Returns:
            dict[str, any]: The loaded entity data
        """
        pass
    
    @abstractmethod
    def validate_alarm(self, validator: AwsAlarmValidator) -> dict[str, any]:
        """
        Validates a complete CloudWatch alarm configuration.
        
        Args:
            validator (AwsAlarmValidator): The validator instance with configuration
        """
        pass
    
    @abstractmethod
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        """
        Extract values from AWS resource.
        
        Args:
            resource (dict): The AWS resource
            
        Returns:
            dict[str, str]: Extracted values keyed by placeholder names
            
        Raises:
            ValueError: If the resource has invalid format
        """
        pass
    
    @abstractmethod
    def get_required_alarm_keys(self) -> list[str]:
        """
        Get the list of required keys for alarms.
        
        Returns:
            list[str]: List of required alarm keys
        """
        pass
    
    @abstractmethod
    def get_optional_alarm_keys(self) -> list[str]:
        """
        Get the list of optional keys for alarms.
        
        Returns:
            list[str]: List of optional alarm keys
        """
        pass
    
    
    def load_resource_values(self, id: str) -> dict[str, str]:
        """
        Convenience method that loads an entity by ID and extracts its resource values.
        
        This method combines load_entity and get_resource_values operations to simplify
        resource value extraction directly from an entity ID.
        
        Args:
            id (str): The identifier of the entity to load
            
        Returns:
            dict[str, str]: Extracted values keyed by placeholder names
        """
        return self.get_resource_values(self.load_entity(id))
