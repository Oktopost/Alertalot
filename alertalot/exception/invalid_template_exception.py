class InvalidTemplateException(Exception):
    """
    Exception raised when a template file has validation issues.
    
    This exception stores both the template filename and a list of specific issues
    encountered during validation.
    
    Attributes:
        __issues (list[str]): List of validation issues found in the template.
        __template (str): Path or name of the template file with issues.
    """
    
    def __init__(self, template: str, issues: list[str]):
        """
        Initialize the InvalidTemplateException with template information and issues.
        
        Args:
            template (str): Path or name of the template file with issues.
            issues (list[str]): List of validation issues found in the template.
        """
        self.__issues = issues
        self.__template = template
 
    
    def __str__(self):
        """
        Return a string representation of the exception.
        
        Returns:
            str: A formatted string containing the template name and all issues,
                 with each issue prefixed by ' > '.
        """
        return (
            f"Issues encountered in the template file {self.__template}. \n"
            "\n > ".join(self.__issues))
    
    @property
    def issues(self) -> list[str]:
        """
        Get the list of validation issues.
        
        Returns:
            list[str]: List of validation issues found in the template.
        """
        return self.__issues
