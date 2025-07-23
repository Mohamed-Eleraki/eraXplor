# Tutorials

# 1. Setup eraXplor for your AWS Account

This tutorial walks you through setting up `eraXplor-aws` to start exporting your AWS cost data automatically.

## Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configure AWS Profile](https://docs.aws.amazon.com/cli/latest/reference/configure/)
- [Python version >= 3.12.3](https://www.python.org/downloads/)

    Check that by:

```bash
python3 --version
```

## Steps

1. **Install eraXplor:**

```bash
pip install eraXplor
```

2. **Run eraXplor:**

```bash
eraXplor-aws
```

```bash
eraXplor-aws <--start-date [yyyy-MM-DD]> <--end-date [yyyy-MM-DD]> \
<--profile [PROFILE-NAME]> \
<--groupby [LINKED_ACCOUNT | SERVICE | PURCHASE_TYPE | USAGE_TYPE | LINKED_ACCOUNT-With-SERVICE | LINKED_ACCOUNT-With-PURCHASE_TYPE | LINKED_ACCOUNT-With-USAGE_TYPE]> \
<--out [file.csv]>
<--granularity [DAILY | MONTHLY]>
```

For Windows/PowerShell users restart your terminal, and you may need to use the following command:

```bash
python3 -m eraXplor-aws

# Or
python -m eraXplor-aws

# to avoid using this command, apend the eraXplor to your paths.
# Normaly its under: C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<version>\Scripts\
```

???+ info "Note"

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*

### Argument Reference

- `--start-date` or `-s`: **_(Optional)_** Default value set as six months before.
- `--end-date` or `-e`: **_(Optional)_** Default value set as Today date.
- `--profile` or `-p`: **_(Optional)_** Default value set as default.
- `--groupby` or `-g`: **_(Optional)_** Default value set as `LINKED_ACCOUNT`.
    The available options are (`LINKED_ACCOUNT`, `SERVICE`, `PURCHASE_TYPE`, `USAGE_TYPE`, `LINKED_ACCOUNT-With-SERVICE`, `LINKED_ACCOUNT-With-PURCHASE_TYPE`, `LINKED_ACCOUNT-With-USAGE_TYPE`)
- `--out` or `-o`: **_(Optional)_** Default value set as `cost_repot.csv`.
- `--granularity` or `-G`: **_(Optional)_** Default value set as `MONTHLY`.
    The available options are (`MONTHLY`, `DAILY`)

<!-- This part of the project documentation focuses on a
**learning-oriented** approach. You'll learn how to
get started with the code in this project.

> **Note:** Expand this section by considering the
> following points:

- Help newcomers with getting started
- Teach readers about your library by making them
    write code
- Inspire confidence through examples that work for
    everyone, repeatably
- Give readers an immediate sense of achievement
- Show concrete examples, no abstractions
- Provide the minimum necessary explanation
- Avoid any distractions -->