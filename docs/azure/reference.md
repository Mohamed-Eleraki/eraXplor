# Azure - Reference

This section provides a structured breakdown of the main application module and its supporting utilities used in the `eraXplor_azure` project.

[eraXplor source code](https://github.com/Mohamed-Eleraki/eraXplor/tree/master/src/eraXplor_azure)

---

## Main Application Module

### Entry Point

::: eraXplor_azure.__main__

This is the primary script responsible for orchestrating the user workflow. It handles user input, invokes Azure cost data retrieval, and manages data export functionality.

---

## Utility Modules

### Banner Utilities

::: eraXplor_azure.utils.banner_utils

Responsible for rendering styled ASCII banners and displaying copyright
information used in the CLI interface.

---

### Cost Export Utilities

::: eraXplor_azure.utils.cost_export_utils

Contains functions for retrieving cost and usage reports from Azure Cost Explorer using `CostManagementClient`

---

### CSV Export Utilities

::: eraXplor_azure.utils.csv_export_utils

Provides functionality to export retrieved cost data into a structured CSV format.

