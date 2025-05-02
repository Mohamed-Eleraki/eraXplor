# 📚 Reference

This section provides a structured breakdown of the main application module and its supporting utilities used in the `eraXplor` project.

---

## 🔹Main Application Module

### ▶️ Entry Point

::: eraXplor.__main__

This is the primary script responsible for orchestrating the user workflow. It handles user input, invokes AWS cost data retrieval, and manages data export functionality.

---

## 🛠 Utility Modules

### 🎨 Banner Utilities

::: eraXplor.utils.banner_utils

Responsible for rendering styled ASCII banners and displaying copyright
information used in the CLI interface.

---

### 📊 Cost Export Utilities

::: eraXplor.utils.cost_export_utils

Contains functions for retrieving cost and usage reports from AWS Cost Explorer using `boto3`, grouped by various dimensions such as:

- Linked AWS accounts
- AWS services
- Purchase types
- Usage types

---

### 🧾CSV Export Utilities

::: eraXplor.utils.csv_export_utils

Provides functionality to export retrieved cost data into a structured CSV format.

---

### 📅 Date Utilities

::: eraXplor.utils.date_utils

Includes interactive functions for prompting and validating date input from users, ensuring format compliance and error handling.

---