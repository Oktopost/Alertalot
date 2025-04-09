class InvalidTemplateException(Exception):
    def __init__(self, template: str, issues: list[str]):
        self.__issues = issues
        self.__template = template
 
    
    def __str__(self):
        return (
            f"Issues encountered in the template file {self.__template}. \n"
            "\n > ".join(self.__issues))
    
    @property
    def issues(self) -> list[str]:
        return self.__issues
