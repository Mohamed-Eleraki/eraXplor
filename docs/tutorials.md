# Tutorials


# 1. Setup eraXplor for your AWS Account

This tutorial walks you through setting up `eraXplor` to start exporting your AWS cost data automatically.

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

???+ info "Note"

    Ensure you run the command in a place you have sufficient permission to replace file.
    *The eraXport tool sorting cost reult into a CSV file, by default The CSV will replace for next run.*

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