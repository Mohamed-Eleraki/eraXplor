![https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/eraXplor.jpeg](https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/eraXplor.jpeg)

AWS Cost Export Tool for automated cost reporting and analysis.

**eraXplor** is an automated AWS cost reporting tool designed for assest DevOps and FinOps teams fetching and sorting AWS Cost Explorer.
it extracts detailed cost data by calling AWS Cost Explorer API directly and Transform result as a CSV.
`eraXplor` gives you the ability to sort the cost by Account, Service, Usage Type or even By Purchase Type.
as well as format and separate the result by Monthly or Daily cost.

## Key Features

- ✅ **Account-Level Cost Breakdown**: Monthly or daily unblended costs per linked account.
- ✅ **Service-Level Cost Breakdown**: Monthly or daily unblended costs per Services.
- ✅ **Purchase Type-Level Cost Breakdown**: Monthly or daily unblended costs per Purchase Type.
- ✅ **Usage Type-Level Cost Breakdown**: Monthly or daily unblended costs per Usage Type.
- ✅ **Flexible Date Ranges**: Custom start/end dates with validation.
- ✅ **Multi-Profile Support**: Works with all configured AWS profiles.
- ✅ **CSV Export**: Ready-to-analyze reports in CSV format.
- ✅ **Cross-platform CLI Interface**: Simple terminal-based workflow, and **Cross OS** platform.
- ✅ **Documentation Ready**: Well explained documentations assest you kick start rapidly.
- ✅ **Open-Source**: the tool is open-source under Apache 2.0 license, which enables your to enhance it for your purpose.

---

## Table Of Contents

Quickly find what you're looking for:

1. [Welcome to eraXplor](https://mohamed-eleraki.github.io/eraXplor/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/how-to-guides/)
4. [Explanation](https://mohamed-eleraki.github.io/eraXplor/explanation/)
5. [Reference](https://mohamed-eleraki.github.io/eraXplor/reference/)

---

## Why eraXplor?

![https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/why_eraXplor.jpeg](https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/why_eraXplor.jpeg)

# How-To Guides

## AWS Profile Configuration

- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) - Command line tool.
- Create an AWS AMI user then extract Access ID & key.
- Configure AWS CLI profile by:

```bash
aws configure <--profile [PROFILE_NAME]>
# ensure you set a defalut region.
```

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

## How-To use

`eraXplor` have multiple arguments set with a default values _-explained below-_, Adjsut these arguments as required.

```bash
eraXplor <--start-date [yyyy-MM-DD]> <--end-date [yyyy-MM-DD]> \
<--profile [PROFILE-NAME]> \
<--groupby [LINKED_ACCOUNT | SERVICE | PURCHASE_TYPE | USAGE_TYPE]> \
<--out [file.csv]>
<--granularity [DAILY | MONTHLY]>
```

For Windows/PowerShell users restart your terminal, and you may need to use the following command:

```bash
python3 -m eraXplor

# Or
python -m eraXplor

# to avoid using this command, apend the eraXplor to your paths.
# Normaly its under: C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<version>\Scripts\
```

<details open>
<summary><strong> ℹ️ Notes </strong></summary>

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*
</details>

### Argument Reference

- `--start-date`, `-s`: **_(Not_Required)_** Default value set as six months before.
- `--end-date`, `-e`: **_(Not_Required)_** Default value set as Today date.
- `--profile`, `-p`: **_(Not_Required)_** Default value set as default.
- `--groupby`, `-g`: **_(Not_Required)_** Default value set as LINKED_ACCOUNT.
    The available options are (`LINKED_ACCOUNT`, `SERVICE`, `PURCHASE_TYPE`, `USAGE_TYPE`)
- `--out`, `-o`: **_(Not_Required)_** Default value set as `cost_repot.csv`.
- `--granularity`, `-G`: **_(Not_Required)_** Default value set as `MONTHLY`.
    The available options are (`MONTHLY`, `DAILY`)

<!-- ```mermaid
graph LR
    A[AWS Console] ->|Complex UI| B[Manual Export]
    B -> C[Spreadsheet Manipulation]
    D[eraXplor] ->|Automated| E[Standardized Reports]
    style D fill:#4CAF50,stroke:#388E3C
    Replace -> with double --
``` -->
<br><br>
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
