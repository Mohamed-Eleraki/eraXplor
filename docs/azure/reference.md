# Azure - Reference

This section documents the current Azure FOCUS workflow modules used by `eraXplor`.

[eraXplor source code](https://github.com/Mohamed-Eleraki/eraXplor/tree/master/src/core/services/azure)

---

## Main Application Module

### Entry Point

::: core.services.azure

This is the primary script responsible for orchestrating the user workflow. It handles user input, invokes Azure cost data retrieval, and manages data export functionality.

---

## Utility Modules

### Banner Utilities

::: core.services.utils.banner_utils

Responsible for rendering styled ASCII banners and displaying copyright
information used in the CLI interface.

---

### Cost Export Utilities

::: core.services.azure.utils.cost_export_utils

Contains functions for retrieving cost and usage reports from Azure Cost Explorer using `CostManagementClient`

---

### CSV Export Utilities

::: core.services.azure.utils.csv_export_utils

Provides functionality to export retrieved cost data into a structured CSV format.

---

### Resource Provisioning Utilities

::: core.services.azure.utils.focus_depends

Creates the Azure resource group, storage account, container, and folder
required by the export workflow.

---

### Export Configuration Utilities

::: core.services.azure.utils.focus_export_utils

Contains the helpers that discover billing identifiers and create Azure FOCUS
export definitions.

---

### Fetch Utilities

::: core.services.azure.utils.focus_fetch

Provides functionality for downloading generated Parquet export files from the
configured Azure Storage container.

