"""Module for fetching FOCUS Parquet files from AWS S3."""

import os
import boto3
from botocore.exceptions import ClientError

def _resolve_focus_bucket_name(
	session: boto3.Session,
	stack_name: str,
	region: str,
) -> str:
	"""Resolve destination S3 bucket from stack outputs."""
	cloudformation = session.client("cloudformation", region_name=region)
	try:
		resources = cloudformation.describe_stack_resources(StackName=stack_name)["StackResources"]
	except ClientError as exc:
		error_code = exc.response.get("Error", {}).get("Code", "")
		message = str(exc)
		if error_code == "ValidationError" and "does not exist" in message:
			raise ValueError(
				f"CloudFormation stack '{stack_name}' was not found in region '{region}'. "
				"Run '--command configure' first or pass '--stack-name' with an existing stack."
			) from exc
		raise

	bucket_resources = [
		resource
		for resource in resources
		if resource.get("ResourceType") == "AWS::S3::Bucket"
	]

	if not bucket_resources:
		raise ValueError(
			f"No S3 bucket found in stack '{stack_name}'. Provide bucket_name explicitly."
		)

	return bucket_resources[0]["PhysicalResourceId"]


def _resolve_focus_prefix(
	session: boto3.Session,
	stack_name: str,
	region: str,
) -> str:
	"""Resolve FOCUS object prefix from stack parameters using ResourcePrefix."""
	cloudformation = session.client("cloudformation", region_name=region)
	try:
		stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
	except ClientError as exc:
		error_code = exc.response.get("Error", {}).get("Code", "")
		message = str(exc)
		if error_code == "ValidationError" and "does not exist" in message:
			raise ValueError(
				f"CloudFormation stack '{stack_name}' was not found in region '{region}'. "
				"Run '--command configure' first or pass '--stack-name' with an existing stack."
			) from exc
		raise
	parameters = {
		parameter["ParameterKey"]: parameter["ParameterValue"]
		for parameter in stack.get("Parameters", [])
	}

	resource_prefix = parameters.get("ResourcePrefix", "cid")
	return f"{resource_prefix}/focus"


def download_parquet_files(
	profile_name: str = "default",
	region: str = "us-east-1",
	stack_name: str = "CID-DataExports-Source",
) -> list[str]:
	"""
	Downloads FOCUS Parquet files from AWS S3.

	Args:
		profile_name: AWS profile name.
		region: AWS region where the stack is deployed.
		stack_name: CloudFormation stack name that owns FOCUS resources.

	Returns:
		List of paths to the downloaded Parquet files.
	"""

	local_download_path = "./downloaded_parquet_files"
	os.makedirs(local_download_path, exist_ok=True)

	session = boto3.Session(profile_name=profile_name, region_name=region)
	s3_client = session.client("s3", region_name=region)

	resolved_bucket_name = _resolve_focus_bucket_name(
		session=session,
		stack_name=stack_name,
		region=region,
	)
	resolved_folder_name = _resolve_focus_prefix(
		session=session,
		stack_name=stack_name,
		region=region,
	)
	prefix = resolved_folder_name.rstrip("/") + "/"

	print(
		f"Listing objects in bucket '{resolved_bucket_name}' under prefix '{prefix}'..."
	)

	downloaded_files = []
	paginator = s3_client.get_paginator("list_objects_v2")

	for page in paginator.paginate(Bucket=resolved_bucket_name, Prefix=prefix):
		for obj in page.get("Contents", []):
			key = obj["Key"]

			if key.endswith("/") or not key.lower().endswith(".parquet"):
				continue

			download_file_path = os.path.join(local_download_path, os.path.basename(key))
			s3_client.download_file(resolved_bucket_name, key, download_file_path)
			downloaded_files.append(download_file_path)
			print(f"Downloaded: {download_file_path}")

	if not downloaded_files:
		raise FileNotFoundError(
			"No Parquet files were found in the configured FOCUS bucket/prefix."
		)

	return downloaded_files

