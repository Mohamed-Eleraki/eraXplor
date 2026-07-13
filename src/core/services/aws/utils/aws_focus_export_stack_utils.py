"""Utility functions for automating AWS Data Exports using CID CloudFormation."""

from typing import Any
import re
import boto3
from botocore.exceptions import ClientError, WaiterError


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


def _is_bucket_name_in_use(session: boto3.Session, region: str, bucket_name: str) -> bool:
	"""Return True when an S3 bucket name is already in use."""
	s3_client = session.client("s3", region_name=region)
	try:
		s3_client.head_bucket(Bucket=bucket_name)
		return True
	except ClientError as exc:
		error_code = str(exc.response.get("Error", {}).get("Code", ""))
		if error_code in {"404", "NoSuchBucket", "NotFound"}:
			return False
		if error_code in {"403", "AccessDenied", "301", "PermanentRedirect"}:
			return True
		return True


def _get_stack_failure_reason(cloudformation: Any, stack_name: str) -> str:
	"""Best-effort extraction of the most relevant stack failure reason."""
	try:
		events = cloudformation.describe_stack_events(StackName=stack_name)["StackEvents"]
		for event in events:
			status = event.get("ResourceStatus", "")
			if status.endswith("_FAILED") or status in {"ROLLBACK_IN_PROGRESS", "ROLLBACK_COMPLETE"}:
				logical_id = event.get("LogicalResourceId", "UnknownResource")
				reason = event.get("ResourceStatusReason", "Unknown failure reason")
				return f"{logical_id}: {reason}"
	except Exception:
		pass
	return "No detailed stack event failure reason was returned by CloudFormation."


def build_focus_stack_parameters(
	destination_account_id: str,
	source_account_ids: list[str] | None = None,
	resource_prefix: str = "cid",
	focus_time_granularity: str = "DAILY",
) -> list[dict[str, str]]:
	"""Build CloudFormation parameters for CID Data Exports stack (FOCUS only).

	Args:
		destination_account_id: AWS account ID where exports are delivered.
		source_account_ids: AWS account IDs to collect exports from.
		resource_prefix: Prefix for all CID-created AWS resources.
		focus_time_granularity: Export time granularity. One of HOURLY, DAILY,
			MONTHLY. Changing this after initial deployment requires a full stack
			redeployment and data purge. Defaults to MONTHLY.
	"""
	parameters = [
		{"ParameterKey": "DestinationAccountId", "ParameterValue": destination_account_id},
		{"ParameterKey": "ResourcePrefix", "ParameterValue": resource_prefix},
		{"ParameterKey": "ManageCUR2", "ParameterValue": "no"},
		{"ParameterKey": "ManageFOCUS", "ParameterValue": "yes"},
		{"ParameterKey": "ManageCOH", "ParameterValue": "no"},
		{"ParameterKey": "ManageCarbon", "ParameterValue": "no"},
		{"ParameterKey": "LegacyLocalBucket", "ParameterValue": "no"},
		{"ParameterKey": "FOCUSTimeGranularity", "ParameterValue": focus_time_granularity},
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
	focus_time_granularity: str = "MONTHLY",
	wait: bool = True,
) -> dict[str, Any]:
	"""
	Deploy or update the CID Data Exports CloudFormation stack for FOCUS exports.

	This uses the AWS-managed CloudFormation template from the Cloud Intelligence
	Dashboards guidance and enables only FOCUS export management.

	Full list of CloudFormation template parameters and their defaults:

	Parameter                  | Template default        | This utility
	---------------------------|-------------------------|------------------------------
	DestinationAccountId       | (required)              | current account or arg
	ResourcePrefix             | "cid"                   | "cid"
	ManageCUR2                 | (required) yes/no       | "no"  (FOCUS only)
	ManageFOCUS                | (required) yes/no       | "yes"
	ManageCOH                  | (required) yes/no       | "no"
	ManageCarbon               | (required) yes/no       | "no"
	SourceAccountIds           | (optional, comma list)  | current account or arg
	FOCUSTimeGranularity       | "HOURLY"                | "MONTHLY" (configurable)
	CUR2TimeGranularity        | "HOURLY"                | not passed (not used)
	LegacyLocalBucket          | "yes"                   | "no"  (fresh deployments)
	SecondaryDestinationBucket | ""                      | not passed (not used)
	LakeFormationEnabled       | "no"                    | not passed (template default)
	EnableSCAD                 | yes/no                  | not passed (template default)
	EnableIAMPrincipalData     | yes/no                  | not passed (template default)
	RolePath                   | "/"                     | not passed (template default)
	AddScheduleForBlockingWrite| "no"                    | not passed (template default)
	DisableWriteCronSchedule   | "0 1 * * ? *"           | not passed (template default)
	EnableWriteCronSchedule    | "0 3 * * ? *"           | not passed (template default)

	Note: changing focus_time_granularity on an existing stack requires a full
	stack redeployment, data purge in the destination bucket, and a backfill
	request to AWS. Do not change it lightly after initial deployment.
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
		focus_time_granularity=focus_time_granularity,
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
		destination_bucket_name = f"{resource_prefix}-{account_id}-data-exports"
		if _is_bucket_name_in_use(session, region, destination_bucket_name):
			raise ValueError(
				f"Resource conflict: AWS::S3::Bucket '{destination_bucket_name}' "
				"already exists. "
				f"Stack '{stack_name}' does not exist, so this run is in create mode "
				"(not update mode). "
				"Use the existing stack name to update, choose a different "
				"resource_prefix, or delete/empty old retained resources first."
			)

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
		try:
			cloudformation.get_waiter(waiter_name).wait(StackName=stack_name)
		except WaiterError as exc:
			stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
			stack_status = stack.get("StackStatus", "UNKNOWN")
			stack_status_reason = stack.get("StackStatusReason", "")
			failure_reason = _get_stack_failure_reason(cloudformation, stack_name)
			raise ValueError(
				f"CloudFormation stack '{stack_name}' {action} failed with status "
				f"'{stack_status}'. "
				f"Reason: {stack_status_reason or failure_reason}. "
				"Review stack events in AWS Console, fix the issue, then rerun configure."
			) from exc

	stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
	return {
		"action": action,
		"stack_name": stack_name,
		"stack_id": stack_id,
		"stack_status": stack["StackStatus"],
		"parameters": parameters,
	}

