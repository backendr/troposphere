# Cloudformation VPC Generator Example
An example of how to use [Troposphere](https://github.com/cloudtools/troposphere) to generate [Cloudformation](https://aws.amazon.com/cloudformation/) files.

This example will produce a simple VPC with naming specified via the `env` argument.

Validation of the output can be performed with [cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint):
```
./service_vpc.py <env> [options] > filename.[json|yaml] && cfn-lint filename.[json|yaml]
```


### Requirements
+ Python3
+ Troposphere

If you are a PIP user, you can run `pip install -r requirements.txt` from the project root, or install manually.

### Usage

```
service_vpc.py [-h] [-y] env

Generates Service VPC Cloudformation. Default output is JSON.

positional arguments:
  env               Name of environment

optional arguments:
  -h, --help        show this help message and exit
  -y, --yaml        Output to JSON
```
    
### Output
Outputs the generated VPC Cloudformation in `JSON`, unless the `-y, --yaml` flag is provided.

You can save to a file with `./service_vpc.py <env> [options] > filename.[json|yaml]`