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

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure AWS credentials:**

```bash
aws configure --profile [PROFILE_NAME]
```

3. **Run the tool:**

```bash
python main.py
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