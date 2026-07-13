# Welcome to eraXplor

Cost Export Tool for automated cost reporting and analysis.

**eraXplor** is an automated cost reporting tool designed for assist DevOps and FinOps teams fetching and sorting AWS and Azure Cost Explorer.
it extracts detailed cost data by calling natively cloud provider APIs directly and Transform result into CSV file.
`eraXplor` gives you the ability to sort the cost with wide range of options:

- For **AWS** you able to sort cost by Account, Service, Usage Type or even By Purchase Type; as well as format and separate the result by Monthly or Daily.
- For **Azure** you able to sort cost by Subscription, as well as format and separate the result by Monthly or Daily.
</br>


## Key Features

- **Cloud provider Separated tools**: Separated tool for each cloud provider _(e.g. AWS and Azure)_ avoiding complexity.
- **Flexible Date Ranges**: Custom start/end dates with validation.
- **Multi-Profile Support**: Works with all configured AWS profiles.
- **Multi-Subscription Support**: Works to list all configured Azure subscriptions.
- **Enhanced Grouping Options**: Advanced grouping for AWS (Account+Service, Account+Purchase Type, Account+Usage Type) and Azure (Subscriptions, Services, Resource groups).
- **REST API Support**: FastAPI-based REST API for programmatic cost data access with JSON responses.
- **CSV Export**: Ready-to-analyze reports in CSV format.
- **Cross-platform CLI Interface**: Simple terminal-based command-line, and **Cross OS** platform.
- **Documentation Ready**: Well explained documentations assist you kick start rapidly.
- **Open-Source**: the tool is open-source under Apache 2.0 license, which enables your to enhance it for your purpose.

## Table Of Contents

Quickly find what you're looking for depending on
your use case by looking at the different pages.

### AWS

1. [Overview](https://mohamed-eleraki.github.io/eraXplor/aws/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/aws/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/aws/how-to-guides/)
5. [Concepts & Explanation](https://mohamed-eleraki.github.io/eraXplor/aws/explanation/)
6. [Refrence]()
7. [API](https://mohamed-eleraki.github.io/eraXplor/api/aws/)
8. [API Refrence](https://mohamed-eleraki.github.io/eraXplor/api/aws-reference/)

### Azure

1. [Overview](https://mohamed-eleraki.github.io/eraXplor/azure/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/azure/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/azure/how-to-guides/)
5. [Concepts & Explanation](https://mohamed-eleraki.github.io/eraXplor/azure/explanation/)
6. [Refrence](https://mohamed-eleraki.github.io/eraXplor/azure/reference/)
7. [API](https://mohamed-eleraki.github.io/eraXplor/api/azure/)
8. [API Refrence](https://mohamed-eleraki.github.io/eraXplor/api/azure-reference/)
</br>

# How-To Guides

## Check installed Python version

- Ensure you Python version is >= 3.12.3 by:

```bash
python --version

# Consider update Python version if less than 3
```

## Install eraXplor

- Install eraXplor too by:

```bash
pip install eraXplor
```

## REST API

eraXplor includes a FastAPI-based REST API that allows you to programmatically export cost data from both AWS and Azure.


### Start the API Server

```bash
# From the repository root
uvicorn api.main:app --app-dir src --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
Interactive API test `Swagger UI` under `http://localhost:8000/docs`

### API Endpoints

#### AWS FOCUS Workflow

**POST /aws/focus/run**

```bash
curl -X POST "http://localhost:8000/aws/focus/run" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "configure",
    "profile": "default",
    "region": "us-east-1",
    "stack_name": "CID-DataExports-Source",
    "granularity": "MONTHLY"
  }'
```

**GET /aws/focus/run**

```bash
curl "http://localhost:8000/aws/focus/run?command=download&profile=default&region=us-east-1&stack_name=CID-DataExports-Source"
```

#### Azure Cost Export

**POST /azure/cost/export**

```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-01-01",
    "end_date": "2025-03-30",
    "granularity": "Monthly",
    "group_by": "subscription"
  }'
```

**GET /azure/cost/export**

```bash
curl "http://localhost:8000/azure/cost/export?start_date=2025-01-01&end_date=2025-03-30&granularity=Monthly&group_by=subscription"
```

### API Response Format

```json
{
  "success": true,
  "message": "AWS cost data exported successfully",
  "total_records": 5,
  "cost_data": [...],
  "request_parameters": {
    "start_date": "2025-01-01",
    "end_date": "2025-03-30",
    "profile": "default",
    "group_by": "LINKED_ACCOUNT",
    "granularity": "MONTHLY"
  }
}
```

### API Documentation (Swagger UI)

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## How-To-Guide - AWS

### AWS profile configuration

- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) - Command line tool.
- Create an AWS AMI user then extract Access ID & key.
- Configure AWS CLI profile by:

```bash
aws configure <--profile [PROFILE_NAME]>
# ensure you set a defalut region.
```

### How-To use - AWS

`eraXplor-aws` now supports two separate commands for AWS FOCUS workflow.

```bash
# Step 1: Configure data export stack
eraXplor-aws --command configure --profile default --region us-east-1 --stack-name CID-DataExports-Source --granularity MONTHLY

# Step 2: Download parquet files later (after export data is available)
eraXplor-aws --command download --profile default --region us-east-1 --stack-name CID-DataExports-Source
```

### Argument Reference - AWS

- `--command`, `-c`: **_(Not Required)_** Default value is `configure`.
  Available options: `configure`, `download`
- `--profile`, `-p`: **_(Not Required)_** Default value is `default`.
- `--region`, `-r`: **_(Not Required)_** Default value is `us-east-1`.
- `--stack-name`, `-s`: **_(Not Required)_** Default value is `CID-DataExports-Source`.
- `--granularity`, `-g`: **_(Not Required)_** Default value is `MONTHLY`.
  Available options: `HOURLY`, `DAILY`, `MONTHLY`

### Example Usage - AWS

```bash
eraXplor-aws
```

---

## How-To-Guide - Azure

## Azure CLI Authentication

- Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt) - Command line tool by specifing your attended OS.
- ensure your account have sufficient permission as `Billing Reader` or `Usage Billing Contributor` to manage Azure billing.
- Check installed package by:

```bash
az --version
```

- Authenticate using your Azure account:

```bash
az login
```

This will open the portal in your default browser to authenticate.

### How-To use - Azure

`eraXplor-azure` have multiple arguments set with a default values _-explained below-_, Adjsut these arguments as required.

```bash
eraXplor_az <--start-date [yyyy,MM,DD]> <--end-date [yyyy,MM,DD]> \
<--subscription_id [SUBSCRIPTION_ID]> \
<--group-by [subscription | ServiceName | ResourceGroupName]> \
<--granularity [DAILY | MONTHLY]> \
<--output [FILE_NAME.CSV]>
```

### Argument Reference - Azure

- `--start-date` or `-s`: **_(Optional)_** Default value set as three months before.
- `--end-date` or `-e`: **_(Optional)_** Default value set as Today date.
- `--group-by` or `-g`: **_(Optional)_** Default value set as `subscription`.
    Available options: (`subscription`, `ServiceName`, `ResourceGroupName`)
- `--out` or `-o`: **_(Optional)_** Default value set as `az_cost_report.csv`.
- `--granularity` or `-G`: **_(Optional)_** Default value set as `MONTHLY`.
    The available options are (`MONTHLY`, `DAILY`)

### Azure Commands

### Example Usage - Azure

```bash
eraXplor-azure
```

---

For Windows/PowerShell users restart your terminal, and you may need to use the following command:

```bash
python -m eraXplor-aws

# Or
python -m eraXplor-azure

# to avoid using this command, apend the eraXplor to your paths.
# Normaly its under: C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<version>\Scripts\
```

## About the Author

<details open>
<summary><strong>👋Show/Hide Author Details👋</strong></summary>

**Mohamed eraki**  
_Cloud & DevOps Consultant_

[![Email](https://img.shields.io/badge/Contact-mohamed--ibrahim2021@outlook.com-blue?style=flat&logo=mail.ru)](mailto:mohamed-ibrahim2021@outlook.com)  
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-informational?style=flat&logo=linkedin)](https://www.linkedin.com/in/mohamed-el-eraki-8bb5111aa/)  
[![Blog](https://img.shields.io/badge/Blog-Visit-brightgreen?style=flat&logo=rss)](https://eraki.hashnode.dev/)

### Project Philosophy

> "I built eraXplor to solve real-world cloud cost visibility challenges — the same pain points I encounter daily in enterprise environments. This tool embodies my belief that financial accountability should be accessible to every technical team."

</details>

