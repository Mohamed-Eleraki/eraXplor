"""
Module for installing dependencies required for AWS FOCUS data export.

This module provides functions to create necessary AWS resources for FOCUS data export, including:
- S3 Bucket
- Folder (Virtual Directory / Prefix) within the S3 Bucket

ARGS:
- bucket_name: Name of the S3 bucket to create
- region: AWS region for the resources
- folder_name: Name of the Folder (Prefix) to create within the S3 Bucket

Dependencies:
- boto3
"""

import boto3
from botocore.exceptions import ClientError


def create_s3_bucket(
    bucket_name: str,
    region: str = "us-east-1",
) -> None:
    """
    Creates an S3 bucket if it does not already exist.
    """

    s3_client = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print(f"S3 bucket '{bucket_name}' already exists.")
        else:
            raise


def create_s3_bucket_folder(
    bucket_name: str,
    region: str = "us-east-1",
    folder_name: str = "focus-exports",
) -> None:
    """
    Creates a folder (prefix / virtual directory) inside the S3 bucket.
    """

    s3_client = boto3.client("s3", region_name=region)

    folder_key = f"{folder_name}/"
    s3_client.put_object(Bucket=bucket_name, Key=folder_key, Body=b"")
    print(f"Folder '{folder_key}' created successfully in bucket '{bucket_name}'.")


def setup_focus_export_dependencies(
    bucket_name: str = "focus-data-export-bucket",
    region: str = "us-east-1",
    folder_name: str = "focus-exports",
) -> None:
    """
    Creates all required AWS resources for FOCUS data export:
    - S3 Bucket
    - Folder (virtual directory / prefix) within the S3 Bucket
    """

    create_s3_bucket(bucket_name=bucket_name, region=region)
    create_s3_bucket_folder(bucket_name=bucket_name, region=region, folder_name=folder_name)


if __name__ == "__main__":
    setup_focus_export_dependencies()
