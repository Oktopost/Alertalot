# Alertalot

<p align="center">
  <img src="docs/alertalot-logo.png" alt="Alertalot Logo" width="128">
</p>

Python library for creating AWS alerts automatically. 


## Code Quality and Testing

Before running any of the following commands, ensure that your virtual environment is activated:

```
source ./venv/bin/activate
```

### Test and Lint Commands

| Task                         | Command                                                 |
|:-----------------------------|:--------------------------------------------------------|
| Run Unit Tests with Coverage | `pytest --cov=alertalot`                                |
| Lint Alertalot Code          | `pylint alertalot --rcfile=.pylintrc --fail-under=10`   |
| Lint Test Code               | `pylint tests --rcfile=tests/.pylintrc --fail-under=10` |
