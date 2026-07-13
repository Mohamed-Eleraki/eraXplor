# AWS - Reference

This section documents the current AWS FOCUS workflow modules used by `eraXplor`.

[eraXplor source code](https://github.com/Mohamed-Eleraki/eraXplor/tree/master/src/core/services/aws)

---

## Main Application Module

### Entry Point

::: core.services.aws

This is the primary CLI entry point for configuring and downloading AWS FOCUS exports.

---

## Utility Modules

### Banner Utilities

::: core.services.utils.banner_utils

Responsible for rendering styled ASCII banners and displaying copyright
information used in the CLI interface.

---

### Parser Utilities

::: core.services.aws.utils.focus_parser_utils

Contains the command parsing helpers used to validate CLI input and normalize
workflow options.

---

### Export Stack Utilities

::: core.services.aws.utils.aws_focus_export_stack_utils

Contains the CloudFormation orchestration helpers that create or update the AWS
FOCUS export infrastructure.

---

### Fetch Utilities

::: core.services.aws.utils.aws_focus_fetch

Provides functionality for downloading generated Parquet export files after the
AWS export pipeline has produced them.

