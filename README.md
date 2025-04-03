# Alertalot

<p align="center">
  <img src="docs/alertalot-logo.png" alt="Alertalot Logo" width="128">
</p>

Python library for creating AWS CloudWatch alerts automatically based on predefined configurations.

## Getting Started

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/alertalot.git
   cd alertalot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source ./venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Alertalot can be run with various options to create CloudWatch alerts for AWS resources.

### Basic Usage

```
python -m alertalot.main --instance-id i-xxxxxxxxx --params-file examples/params.yaml --template-file examples/ec2-application.yaml --region us-east-1
```

### Available Options

| Option | Description |
|:-------|:------------|
| `--instance-id` | ID of an EC2 instance to generate the alerts for |
| `--params-file` | Relative path to the parameters file to use (see examples/params.yaml) |
| `--template-file` | Relative path to the template file to use (see examples/ec2-application.yaml) |
| `--region` | The AWS region to use |
| `--dry-run` | Simulate the requests without executing them |
| `-v, --verbose` | Enable verbose output to show details about executed actions |

### Special Actions

| Action | Description |
|:-------|:------------|
| `--show-parameters, --show-params` | Only loads the parameters file and outputs the result. Parameters for the specified region will be merged with global parameters. |
| `--test-aws` | Only checks if AWS is accessible by calling sts:GetCallerIdentity. Use with `--verbose` to see detailed output. |
| `--show-instance` | Loads and describes the target instance. Requires a valid instance ID. |

## Configuration Files

### Parameters File

The parameters file (YAML or JSON) contains values that will be substituted in the template file:

```yaml
params:
  global:
    # Global parameters used across all regions
  us-east-1:
    # Region-specific parameters
    ALARM_ACTION_ARN: "arn:aws:sns:us-east-1:aaaa:bbbb"
```

### Template File

The template file defines the CloudWatch alarms to be created:

```yaml
alarms:
  - cpu:
      metric-name: AWS / CPU Usage 1 minute / $INSTANCE_NAME / $INSTANCE_ID
      alarm-name: $ALARM_ACTION_ARN
      statistic: Average
      period: 5 minutes
      comparison-operator: GreaterThanOrEqualToThreshold
      threshold: 70%
      evaluation-periods: 1 minute
      tags:
        level: info
      treat-missing-data: breaching
```

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