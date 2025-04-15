from alertalot.exception.invalid_template_exception import InvalidTemplateException


def test__invalid_template_exception__init():
    template_path = "test_template.yaml"
    issues = ["Issue 1", "Issue 2"]
    
    exception = InvalidTemplateException(template_path, issues)
    
    assert exception.issues == issues


def test__invalid_template_exception__str():
    template_path = "test_template.yaml"
    issues = ["Issue 1", "Issue 2"]
    
    exception = InvalidTemplateException(template_path, issues)
    result = str(exception)
    
    assert "test_template.yaml" in result
    assert "Issue 1" in result
    assert "Issue 2" in result
