# Tutorials

# 1. Setup eraXplor for your Azure Authentication

This tutorial walks you through setting up of `eraXplor_az` to start exporting your Azure cost data automatically.

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt)
- [Python version >= 3.12.3](https://www.python.org/downloads/)

    Check that by:

```bash
python3 --version
```

## Steps

1. **Install eraXplor_az:**

```bash
pip install eraXplor
```

2. **Run eraXplor:**

```bash
eraXplor_az -S SUBSCRIPTION_ID
```

```bash
eraXplor_az <--start-date [yyyy,MM,DD]> <--end-date [yyyy,MM,DD]> \
<--subscription_id [SUBSCRIPTION_ID]> \
<--granularity [DAILY | MONTHLY]> \
<--output [FILE_NAME.CSV]>
```

For Windows/PowerShell users restart your terminal, and you may need to use the following command:

```bash
python3 -m eraXplor_az

# Or
python -m eraXplor_az

# to avoid using this command, apend the eraXplor to your paths.
# Normaly its under: C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<version>\Scripts\
```

???+ info "Note"

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*

### Argument Reference

- `--start-date` or `-s`: **_(Optional)_** Default value set as three months before.
- `--end-date` or `-e`: **_(Optional)_** Default value set as Today date.
- `--subscription_id` or `-S`: **_(Required)_** subscription id.
- `--out` or `-o`: **_(Optional)_** Default value set as `az_cost_report.csv`.
- `--granularity` or `-g`: **_(Optional)_** Default value set as `MONTHLY`.
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