# Tutorials

## 1. Setup eraXplor for your Azure Authentication

This tutorial walks you through setting up of `eraXplor-azure` to start exporting your Azure cost data automatically.

### Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt)
- [Python version >= 3.12.3](https://www.python.org/downloads/)

    Check that by:

```bash
python3 --version
```

### Steps

1. **Install eraXplor-azure:**

```bash
pip install eraXplor
```

2. **Azure login**
The Tool support multiple authentication _e.g. Azure CLI login, Managed Identity, etc_. You can login by running the following command:
_it's require to install azure cli first form the link above_

```bash
az login
```

3. **Run eraXplor:**

---

## 2. Usage Examples

### Basic Usage - List All Subscription Costs

```bash
eraXplor-azure
```

This will export costs for all accessible subscriptions grouped by subscription.

### Group by Azure Service Name

View costs breakdown by Azure service (e.g. Virtual Machines, Storage, SQL Database):

```bash
eraXplor-azure -g ServiceName -G Monthly
```

### Group by Resource Group

View costs breakdown by Resource Group for FinOps tagging analysis:

```bash
eraXplor-azure -g ResourceGroupName -G Monthly
```

### Custom Date Range

```bash
eraXplor-azure -s 2025,01,01 -e 2025,03,30
```

### Custom Output Filename

```bash
eraXplor-azure -o my_cost_report.csv
```

---

## 3. Command Reference

```bash
eraXplor-azure <--start-date [yyyy,MM,DD]> <--end-date [yyyy,MM,DD]> \
<--group-by [subscription | ServiceName | ResourceGroupName]> \
<--granularity [Daily | Monthly]> \
<--output [FILE_NAME.CSV]>
```

For Windows/PowerShell users restart your terminal, and you may need to use the following command:

```bash
python3 -m eraXplor-azure

# Or
python -m eraXplor-azure

# to avoid using this command, apend the eraXplor to your paths.
# Normaly its under: C:\Users\<YourUser>\AppData\Local\Programs\Python\Python<version>\Scripts\
```

### Argument Reference

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--start-date` | `-s` | Start date (YYYY,MM,DD format) | 3 months ago |
| `--end-date` | `-e` | End date (YYYY,MM,DD format) | Today |
| `--group-by` | `-g` | Grouping dimension | `subscription` |
| `--granularity` | `-G` | Time aggregation | `Monthly` |
| `--out` | `-o` | Output CSV filename | `az_cost_report.csv` |

### Group By Options

- **`subscription`**: Group costs by Azure subscription (default)
- **`ServiceName`**: Group costs by Azure service name
- **`ResourceGroupName`**: Group costs by Resource Group

### Granularity Options

- **`Monthly`**: Aggregate costs by month (default)
- **`Daily`**: Show daily cost breakdown

???+ info "Note"

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*

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