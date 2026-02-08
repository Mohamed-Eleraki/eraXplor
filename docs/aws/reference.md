# AWS - Reference

This section provides a structured breakdown of the main application module and its supporting utilities used in the `eraXplor_aws` project.

🌟[eraXplor source code](https://github.com/Mohamed-Eleraki/eraXplor/tree/master/src/eraXplor_aws)

---

## 🔹Main Application Module

### ▶️ Entry Point

::: eraXplor_aws.__main__

This is the primary script responsible for orchestrating the user workflow. It handles user input, invokes AWS cost data retrieval, and manages data export functionality.

---

## 🛠 Utility Modules

### 🎨 Banner Utilities

::: eraXplor_aws.utils.banner_utils

Responsible for rendering styled ASCII banners and displaying copyright
information used in the CLI interface.

---

### 📊 Cost Export Utilities

::: eraXplor_aws.utils.cost_export_utils

Contains functions for retrieving cost and usage reports from AWS Cost Explorer using `boto3`, grouped by various dimensions such as:

- Linked AWS accounts
- AWS services
- Purchase types
- Usage types

---

### 🧾 CSV Export Utilities

::: eraXplor_aws.utils.csv_export_utils

Provides functionality to export retrieved cost data into a structured CSV format.

---

### 📅 Date Utilities

::: eraXplor_aws.utils.date_utils

Includes interactive functions for prompting and validating date input from users, ensuring format compliance and error handling.

