# How-To Guides

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

`eraXplor-azure` have multiple arguments set with a default values _-explained below-_, Adjsut these arguments as required.

```bash
eraXplor-azure <--start-date [yyyy,MM,DD]> <--end-date [yyyy,MM,DD]> \
<--subscription_id [SUBSCRIPTION_ID]> \
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

???+ info "Note"

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*

### Argument Reference

- `--start-date` or `-s`: **_(Optional)_** Default value set as three months before.
- `--end-date` or `-e`: **_(Optional)_** Default value set as Today date.
- `--subscription_id` or `-S`: **_(Optional)_** subscription id, Default value set to list all subscriptions with tags.
- `--out` or `-o`: **_(Optional)_** Default value set as `az_cost_report.csv`.
- `--granularity` or `-g`: **_(Optional)_** Default value set as `Monthly`.
    The available options are (`Monthly`, `Daily`)

<!-- 

# Upcomming Features

- Parse args with non-interactive sessions.
- Rich speadsheets content and charts.
- Fetch the top 10 most expensive services. -->

<!--
if you want automatic monthly exports;
- use cron on linux/macOS or Task Scheduler on windows.
- Example `cron` job monthly *i.e. 1st day of the month at 2 AM.*
bash
0 2 1 * * /usr/bin/python3 /path/to/main.py --profile [PROFILE_NAME] -->

<!-- 

This part of the project documentation focuses on a
**problem-oriented** approach. You'll tackle common
tasks that you might have, with the help of the code
provided in this project.

## How To Add Two Numbers?

You have two numbers and you need to add them together.
You're in luck! The `calculator` package can help you
get this done.

Download the code from this GitHub repository and place
the `calculator/` folder in the same directory as your
Python script:

    your_project/
    │
    ├── calculator/
    │   ├── __init__.py
    │   └── calculations.py
    │
    └── your_script.py

Inside of `your_script.py` you can now import the
`add()` function from the `calculator.calculations`
module:

    # your_script.py
    from calculator.calculations import add

After you've imported the function, you can use it
to add any two numbers that you need to add:

    # your_script.py
    from calculator.calculations import add

    print(add(20, 22))  # OUTPUT: 42.0

You're now able to add any two numbers, and you'll
always get a `float` as a result. -->