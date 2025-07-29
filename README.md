# Welcome to eraXplor

Cost Export Tool for automated cost reporting and analysis.

**eraXplor** is an automated cost reporting tool designed for assest DevOps and FinOps teams fetching and sorting AWS and Azure Cost Explorer.
it extracts detailed cost data by calling nativly cloud provider APIs directly and Transform result into CSV file.
`eraXplor` gives you the ability to sort the cost with wide range of options:

- For **AWS** you able to sort cost by Account, Service, Usage Type or even By Purchase Type; as well as format and separate the result by Monthly or Daily.
- For **Azure** you able to sort cost by Subscription, as well as format and separate the result by Monthly or Daily.
</br>

_azure still under development, more features will be added soon._

## Key Features

- ✅ **Cloud provider Separated tools**: Separated tool for each cloud provider _(e.g. AWS and Azure)_ avoiding complexty.
- ✅ **Flexible Date Ranges**: Custom start/end dates with validation.
- ✅ **Multi-Profile Support**: Works with all configured AWS profiles.
- ✅ **Multi-Subscription Support**: Works to list all configured Azure subscriptions.
- ✅ **CSV Export**: Ready-to-analyze reports in CSV format.
- ✅ **Cross-platform CLI Interface**: Simple terminal-based workflow, and **Cross OS** platform.
- ✅ **Documentation Ready**: Well explained documentations assest you kick start rapidly.
- ✅ **Open-Source**: the tool is open-source under Apache 2.0 license, which enables your to enhance it for your purpose.

## Table Of Contents

Quickly find what you're looking for depending on
your use case by looking at the different pages.

### AWS (eraXplor)

1. [Overview](https://mohamed-eleraki.github.io/eraXplor/aws/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/aws/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/aws/how-to-guides/)
5. [Concepts & Explanation](https://mohamed-eleraki.github.io/eraXplor/aws/explanation/)

### Azure (eraXplor_az)

1. [Overview](https://mohamed-eleraki.github.io/eraXplor/azure/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/azure/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/azure/how-to-guides/)
5. [Concepts & Explanation](https://mohamed-eleraki.github.io/eraXplor/azure/explanation/)
</br>

- [Reference](https://mohamed-eleraki.github.io/eraXplor/reference/)

# How-To Guides

## Check installed Python version

- Ensure you Python version is >= 3.12.3 by:

```bash
python --version

# Consider update Python version if less than 3
```

## Install eraXplor

- Install eraxplor too by:

```bash
pip install eraXplor
```

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

`eraXplor-aws` have multiple arguments set with a default values _-explained below-_, Adjsut these arguments as required.

```bash
eraXplor <--start-date [yyyy-MM-DD]> <--end-date [yyyy-MM-DD]> \
<--profile [PROFILE-NAME]> \
<--groupby [LINKED_ACCOUNT | SERVICE | PURCHASE_TYPE | USAGE_TYPE]> \
<--out [file.csv]>
<--granularity [DAILY | MONTHLY]>
```

### Argument Reference - AWS

- `--start-date`, `-s`: **_(Not_Required)_** Default value set as six months before.
- `--end-date`, `-e`: **_(Not_Required)_** Default value set as Today date.
- `--profile`, `-p`: **_(Not_Required)_** Default value set as `default`.
- `--groupby`, `-g`: **_(Not_Required)_** Default value set as LINKED_ACCOUNT.
    The available options are (`LINKED_ACCOUNT`, `SERVICE`, `PURCHASE_TYPE`, `USAGE_TYPE`)
- `--out`, `-o`: **_(Not_Required)_** Default value set as `cost_repot.csv`.
- `--granularity`, `-G`: **_(Not_Required)_** Default value set as `MONTHLY`.
    The available options are (`MONTHLY`, `DAILY`)

## Example Usage - AWS

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
<--granularity [DAILY | MONTHLY]> \
<--output [FILE_NAME.CSV]>
```

### Argument Reference - Azure

- `--start-date` or `-s`: **_(Optional)_** Default value set as three months before.
- `--end-date` or `-e`: **_(Optional)_** Default value set as Today date.
- `--subscription_id` or `-S`: **_(Optional)_** Default value set to list all subscriptions with tags.
- `--out` or `-o`: **_(Optional)_** Default value set as `az_cost_report.csv`.
- `--granularity` or `-g`: **_(Optional)_** Default value set as `MONTHLY`.
    The available options are (`MONTHLY`, `DAILY`)

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
_Cloud & DevOps Engineer_

[![Email](https://img.shields.io/badge/Contact-mohamed--ibrahim2021@outlook.com-blue?style=flat&logo=mail.ru)](mailto:mohamed-ibrahim2021@outlook.com)  
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-informational?style=flat&logo=linkedin)](https://www.linkedin.com/in/mohamed-el-eraki-8bb5111aa/)  
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?style=flat&logo=twitter)](https://x.com/__eraki__)  
[![Blog](https://img.shields.io/badge/Blog-Visit-brightgreen?style=flat&logo=rss)](https://eraki.hashnode.dev/)

### Project Philosophy

> "I built eraXplor to solve real-world cloud cost visibility challenges — the same pain points I encounter daily in enterprise environments. This tool embodies my belief that financial accountability should be accessible to every technical team."

</details>
