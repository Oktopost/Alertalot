import argparse

from alertalot.generic.args_object import ArgsObject
from alertalot.actions import show_config_action


def parse_args() -> ArgsObject:
	parser = argparse.ArgumentParser(
		description="Create Cloudwatch alerts for "
					"AWS resources based on predefined config")
	
	parser.add_argument("--instance-id",	type=str, help="ID of an EC2 instance to generate the alerts for")
	parser.add_argument("--config-file",	type=str, help="Relative path to the configuration file to use")
	parser.add_argument("--template-file",	type=str, help="Relative path to the template file to use")
	
	parser.add_argument("--region",	type=str, help="The AWS region to use")
	
	parser.add_argument(
		"--dry-run",
		type	= bool,
		help	= "Simulate the requests without executing them",
		default	= False)
	
	parser.add_argument(
		"-v", "--verbose",
		action	= "store_true",
		dest	= "verbose",
		help	= "Enable verbose output to show details about executed actions")
	
	parser.add_argument(
		"--show-config",
		action	= "store_true",
		help	= "If passed, ONLY load the config.yaml file and output the result. "
				  "If any region is passed, it will be used while loading the config",
		default	= False)
	
	return ArgsObject(parser.parse_args())


if __name__ == "__main__":
	args_object = parse_args()
	
	if args_object.show_config:
		show_config_action.execute(args_object)
	
	exit(1)

