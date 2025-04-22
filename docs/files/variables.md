# Variables File

## Overview

The variables file is a key component of the Alertalot library that allows you to define variable values which can be substituted into your alarm templates. This provides a flexible way to manage and reuse configurations across different environments and regions.

When Alertalot processes your alarm templates, it substitutes any variable references (in the form of `$VARIABLE_NAME`) with the corresponding values defined in your variables file. This approach enables you to create generic templates that can be customized for different scenarios without modifying the template itself.

## CLI Usage

Specify a variables file using the `--vars-file` argument:

```
alertalot --vars-file ./config/app-servers.yaml
```

You can specify multiple variables files by using the `--vars-file` argument multiple times:

```
alertalot --vars-file ./config/common.yaml --vars-file ./config/app-servers.yaml
```

When multiple files are specified, they are merged in order. If the same variable is defined in multiple files, the value from the last file takes precedence.

## Example

Here's an example of a variables file:

```yaml
params:
  global:
    CPU_LIMIT: 75
    DEFAULT_EVALUATION_PERIODS: 3
    NAMESPACE: "AWS/EC2"
  us-east-1:
    ALARM_ACTION_ARN: "arn:aws:sns:us-east-1:aaaaa:bbbbb"
    REGION_SPECIFIC_THRESHOLD: 90
  us-west-2:
    ALARM_ACTION_ARN: "arn:aws:sns:us-west-2:ccccc:ddddd"
    REGION_SPECIFIC_THRESHOLD: 85
  eu-central-1:
    ALARM_ACTION_ARN: "arn:aws:sns:eu-central-1:eeeee:fffff"
    REGION_SPECIFIC_THRESHOLD: 80
```

## Structure

### `params`

This is a required key and currently the only supported key at the top level of the variables file.

### `params.<global / [region name]>`

Under the `params` key, you can specify variables for different contexts:

- `params.global`: Variables defined here are available regardless of the configured region.
- `params.[region-name]`: Variables specific to an AWS region (e.g., `params.us-east-1`, `params.us-west-2`).

Each region key contains a map that associates variable names with their values. These values should be of type float, integer, or string.

## Variable Resolution

When Alertalot processes your templates, it resolves variables using the following rules:

1. Only variables from the `params.global` section and the configured region section (`params.[region name]`) are used.
2. If a variable exists in both the `params.global` section and the specific region section, the region-specific value takes precedence.

For example, with the following variables file:

```yaml
params:
  global:
    OTHER_KEY: "other"
    MY_KEY: "1"
  us-east-1:
    MY_KEY: "A"
    EASY_KEY: "east"
  us-west-2:
    MY_KEY: "B"
    WEST_KEY: "west"
```

If you run Alertalot with `--region us-west-2`, the available variables would be:

```yaml
OTHER_KEY: "other"
MY_KEY: "B"
WEST_KEY: "west"
```

## Note

Variable references within the variables file itself are not processed. For example, if you define `A: "B $C"` in your variables file, the value of `A` will be the literal string `"B $C"` even if `C` is defined elsewhere in the file.