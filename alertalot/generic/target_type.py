from enum import Enum


class TargetType(Enum):
    """
    Enumeration of supported target type for AWS.
    """
    EC2 = "ec2"
    
    
    @classmethod
    def has(cls, value: str) -> bool:
        """
        Check if a target name is valid and supported.
        
        Args:
            value (str): Target name to check.

        Returns:
            bool: True if target name exists and supported, False otherwise.
        """
        
        return any(value == member.value for member in cls)
    
    @staticmethod
    def require(value: str) -> "TargetType":
        """
        Validate a target name, and if not valid or not supported, raise an exception.
        
        Args:
            value (str): Target name to check.

        Returns:
            TargetType: Target type as Enum if the value is valid. Otherwise, raise an exception.
        
        Raises:
            ValueError: If target name is not invalid or not supported.
        """
        if not TargetType.has(value):
            raise ValueError(f"Target '{value}' is not valid or not supported")
        
        return TargetType(value)
    