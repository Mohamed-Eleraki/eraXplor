# How-To Guides

## AWS Profile Configuration

- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) - Command line tool.
- Create an AWS AMI user then extract Access ID & key.
- Configure AWS CLI profile by:
```bash
aws configure --profile [PROFILE_NAME]  # Replace [PROFILE_NAME] with your profile name
# 2- Input the Access ID & Key as required.
# 3- Specify the defalut region.
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

- Simply run the `eraXplor` Command, Then follow the prompet interactive session with valid inputs:

```bash
eraXplor

# Enter a start date value with YYYY-MM-DD format: 2025-1-1
# Enter an end date value with YYYY-MM-DD format: 2025-3-30
# Enter your AWS Profile name: profile_name
# Enter the cost group by key:
#     Enter [1] to list by 'LINKED_ACCOUNT' -> Default
#     Enter [2] to list by 'SERVICE'
#     Enter [3] to list by 'PURCHASE_TYPE'
#     Enter [4] to list by 'USAGE_TYPE'
#     Press Enter for 'LINKED_ACCOUNT' -> Default:

# Press Enter for list cost per account, Or Enter a number for attending result.
```

- Check CSV file Created.

# Upcomming Features

- Parse args with non-interactive sessions.
- Rich speadsheets content and charts.
- Fetch the top 10 most expensive services.

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