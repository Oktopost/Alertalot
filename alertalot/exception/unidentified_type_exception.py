class UnidentifiedTypeException(Exception):
    """
    Exception raised when the entity type cannot be identified.
    
    This exception is raised when the 'type' field is missing from the configuration file
    and the command-line arguments do not specify an entity.
    """
    
    def __init__(self):
        """
        Initialize the exception object.
        """
        
        super().__init__(
            "'Configuration error: 'type' must be provided either in the config file or by "
            "specifying an entity ID through one of the entity arguments'")
