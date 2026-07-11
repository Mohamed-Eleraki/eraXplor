"""Utility functions for automating AWS Data Exports using CID CloudFormation."""

from typing import Any
import re
import boto3
from botocore.exceptions import ClientError


CID_DATA_EXPORTS_TEMPLATE_URL = (
	"https://aws-managed-cost-intelligence-dashboards.s3.amazonaws.com/cfn/"
	"data-exports-aggregation.yaml"
)

_VALID_STACK_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]{0,127}$")


def _validate_stack_name(stack_name: str) -> None:
	"""Validate CloudFormation stack name constraints."""
	if not _VALID_STACK_NAME_PATTERN.fullmatch(stack_name):
		raise ValueError(
			"Invalid stack_name. Use 1-128 characters, start with a letter, "
			"and include only letters, numbers, and hyphens."
		)


def _get_current_account_id(session: boto3.Session) -> str:
	"""Get AWS account ID from current boto3 session credentials."""
	return session.client("sts").get_caller_identity()["Account"]


def build_focus_stack_parameters(
	destination_account_id: str,
	source_account_ids: list[str] | None = None,
	resource_prefix: str = "cid",
) -> list[dict[str, str]]:
	"""Build CloudFormation parameters for CID Data Exports stack (FOCUS only)."""
	parameters = [
		{"ParameterKey": "DestinationAccountId", "ParameterValue": destination_account_id},
		{"ParameterKey": "ResourcePrefix", "ParameterValue": resource_prefix},
		{"ParameterKey": "ManageCUR2", "ParameterValue": "no"},
		{"ParameterKey": "ManageFOCUS", "ParameterValue": "yes"},
		{"ParameterKey": "ManageCOH", "ParameterValue": "no"},
		{"ParameterKey": "ManageCarbon", "ParameterValue": "no"},
		{"ParameterKey": "LegacyLocalBucket", "ParameterValue": "yes"},
	]

	if source_account_ids:
		parameters.append(
			{
				"ParameterKey": "SourceAccountIds",
				"ParameterValue": ",".join(source_account_ids),
			}
		)

	return parameters


def deploy_focus_stack(
	stack_name: str = "CID-DataExports-Source",
	profile_name: str = "default",
	region: str = "us-east-1",
	destination_account_id: str | None = None,
	source_account_ids: list[str] | None = None,
	resource_prefix: str = "cid",
	wait: bool = True,
) -> dict[str, Any]:
	"""
	Deploy or update the CID Data Exports CloudFormation stack for FOCUS exports.

	This uses the AWS-managed CloudFormation template from the Cloud Intelligence
	Dashboards guidance and enables only FOCUS export management.
	"""
	_validate_stack_name(stack_name)

	session = boto3.Session(profile_name=profile_name, region_name=region)
	cloudformation = session.client("cloudformation", region_name=region)

	account_id = destination_account_id or _get_current_account_id(session)
	if source_account_ids is None:
		source_account_ids = [account_id]

	parameters = build_focus_stack_parameters(
		destination_account_id=account_id,
		source_account_ids=source_account_ids,
		resource_prefix=resource_prefix,
	)

	stack_exists = True
	try:
		cloudformation.describe_stacks(StackName=stack_name)
	except ClientError as exc:
		if "does not exist" in str(exc):
			stack_exists = False
		else:
			raise

	if not stack_exists:
		print(f"Creating CloudFormation stack '{stack_name}' for FOCUS export automation...")
		response = cloudformation.create_stack(
			StackName=stack_name,
			TemplateURL=CID_DATA_EXPORTS_TEMPLATE_URL,
			Capabilities=["CAPABILITY_NAMED_IAM"],
			Parameters=parameters,
		)
		action = "create"
	else:
		print(f"Updating CloudFormation stack '{stack_name}' for FOCUS export automation...")
		try:
			response = cloudformation.update_stack(
				StackName=stack_name,
				TemplateURL=CID_DATA_EXPORTS_TEMPLATE_URL,
				Capabilities=["CAPABILITY_NAMED_IAM"],
				Parameters=parameters,
			)
			action = "update"
		except ClientError as exc:
			message = str(exc)
			if "No updates are to be performed" in message:
				stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
				return {
					"action": "none",
					"stack_name": stack_name,
					"stack_id": stack["StackId"],
					"stack_status": stack["StackStatus"],
					"parameters": parameters,
				}
			raise

	stack_id = response["StackId"]

	if wait:
		waiter_name = "stack_create_complete" if action == "create" else "stack_update_complete"
		cloudformation.get_waiter(waiter_name).wait(StackName=stack_name)

	stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
	return {
		"action": action,
		"stack_name": stack_name,
		"stack_id": stack_id,
		"stack_status": stack["StackStatus"],
		"parameters": parameters,
	}


if __name__ == "__main__":
	result = deploy_focus_stack()
	print(
		f"FOCUS stack {result['action']} completed. "
		f"Stack: {result['stack_name']} | Status: {result['stack_status']}"
	)
