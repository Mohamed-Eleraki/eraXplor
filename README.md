![https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/eraXplor.jpeg](https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/eraXplor.jpeg)

AWS Cost Export Tool for automated cost reporting and analysis.

**eraXplor** is an automated AWS cost reporting tool designed for assest DevOps and FinOps teams fetching and sorting AWS Cost Explorer.
it extracts detailed cost data by calling AWS Cost Explorer API directly and Transform result as a CSV.
`eraXplor` gives you the ability to sort the cost by Account or even By Service, as well as format and separate the result Monthly.

*`eraXplor` is still under enhancement and this is an 'Initial Model'*


## Key Features
- ✅ **Account-Level Cost Breakdown**: Monthly unblended costs per linked account.
- ✅ **Service-Level Cost Breakdown**: Monthly unblended costs per Services.
- ✅ **Flexible Date Ranges**: Custom start/end dates with validation.
- ✅ **Multi-Profile Support**: Works with all configured AWS profiles.
- ✅ **CSV Export**: Ready-to-analyze reports in CSV format.
- ✅ **Cross-platform CLI Interface**: Simple terminal-based workflow, and Cross OS platform.
- ✅ **Documentation Ready**: Well explained documentations assest you to kick start rapidly.
- ✅ **Open-Source**: the tool is open-source under Apache 2.0 license, which enables your to enhance it for your purpose.

## Why eraXplor?
![https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/why_eraXplor.jpeg](https://github.com/Mohamed-Eleraki/eraXplor/blob/master/docs/assets/images/why_eraXplor.jpeg)


## Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configure AWS Profile](https://docs.aws.amazon.com/cli/latest/reference/configure/)
- [Python version >= 3.12.3](https://www.python.org/downloads/)

    Check that by:

```bash
python3 --version

# Consider update Python version if less than 3
```

## Steps

1. **Install eraXplor:**

```bash
pip install eraXplor
```

2. **Run eraXplor:**

```bash
eraXplor
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




This will prompet you with an Interactive session.
Please, Follow the guide below and enter a valied inputs as follows example:
```bash
Enter a start date value with YYYY-MM-DD format: 2025-1-1
Enter an end date value with YYYY-MM-DD format: 2025-3-30
Enter your AWS Profile name: profile_name
Enter the cost group by key:
    Enter [1] to list by 'LINKED_ACCOUNT' -> Default
    Enter [2] to list by 'SERVICE'
    Enter [3] to list by 'PURCHASE_TYPE'
    Enter [4] to list by 'USAGE_TYPE'
    Press Enter for 'LINKED_ACCOUNT' -> Default:

    # Press Enter for list cost per account, Or Enter a number for attending result.
```

<!-- ```mermaid
graph LR
    A[AWS Console] ->|Complex UI| B[Manual Export]
    B -> C[Spreadsheet Manipulation]
    D[eraXplor] ->|Automated| E[Standardized Reports]
    style D fill:#4CAF50,stroke:#388E3C
    Replace -> with double --
``` -->

---


## Table Of Contents
Quickly find what you're looking for depending on
your use case by looking at the different pages.

1. [Welcome to eraXplor](https://mohamed-eleraki.github.io/eraXplor/)
2. [Tutorials](https://mohamed-eleraki.github.io/eraXplor/tutorials/)
3. [How-To Guides](https://mohamed-eleraki.github.io/eraXplor/how-to-guides/)
4. [Explanation](https://mohamed-eleraki.github.io/eraXplor/explanation/)
5. [Reference](https://mohamed-eleraki.github.io/eraXplor/reference/)

---


<details open>
<summary><strong>👋Show/Hide Author Details👋</strong></summary>

**Mohamed eraki**  
*Cloud & DevOps Engineer*

[![Email](https://img.shields.io/badge/Contact-mohamed--ibrahim2021@outlook.com-blue?style=flat&logo=mail.ru)](mailto:mohamed-ibrahim2021@outlook.com)  
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-informational?style=flat&logo=linkedin)](https://www.linkedin.com/in/mohamed-el-eraki-8bb5111aa/)  
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?style=flat&logo=twitter)](https://x.com/__eraki__)  
[![Blog](https://img.shields.io/badge/Blog-Visit-brightgreen?style=flat&logo=rss)](https://eraki.hashnode.dev/)

### Project Philosophy

> "I built eraXplor to solve real-world cloud cost visibility challenges — the same pain points I encounter daily in enterprise environments. This tool embodies my belief that financial accountability should be accessible to every technical team."

</details>






