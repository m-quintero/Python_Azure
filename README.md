
---

# Python_Azure

This repository contains a collection of Python scripts designed to interact with Azure services. Each script is tailored to specific use cases.

# Azure IAM Activity Log Query Tool

This Python script provides a command-line interface to query IAM activity logs in Azure based on specific criteria. It allows users to specify a date, user identifier (Username or GUID), and operation status to efficiently track and audit IAM changes within a given Azure subscription.

## Features

- **Set Azure Environment**: Choose between `AzureCloud` and `AzureUSGovernment` environments.
- **Select Subscription**: Target specific Azure subscription by name or ID.
- **Date Filter**: Specify the exact date to retrieve IAM activity logs.
- **User Filter**: Option to filter logs by a specific user (by Username or GUID).
- **Status Filter**: Filter activity logs by status (`Failed`, `Started`, `Succeeded`), or retrieve all logs if no status is specified.
- **Automated Report Generation**: Generates a formatted output of the activities for reporting and auditing purposes.
- **Author**: michael.quintero@rackspace.com

## Prerequisites

- Python 3.x
- Azure CLI installed and configured on the host machine.
- Appropriate permissions to access and query Azure Monitor logs.

## Setup and Configuration

1. **Clone the Repository**:
   ```bash
   git clone https://github.rackspace.com/michael-quintero/Python_Azure.git
   cd python_azure
   ```

2. **Ensure Azure CLI is Configured**:
   - Run `az login` to log in to your Azure account.
   - Ensure you have the necessary permissions to set subscriptions and query activity logs.

## Usage

1. **Start the Script**:
   ```bash
   python3 iamchecker.py
   ```

2. **Follow On-screen Prompts**:
   - Enter the cloud type (AzureCloud or AzureUSGovernment).
   - Enter the subscription name or ID.
   - Specify the date for which to retrieve logs (format: YYYY-MM-DD).
   - Optional: Enter a Username or GUID to filter by specific user.
   - Optional: Enter a status (`Failed`, `Started`, `Succeeded`) to filter by specific operation results.

## Sample Output

```
Hello,

The user 'john.doe@microsoft.com' made the following IAM updates on the 'Your Subscription Name' donated subscription:

Caller Name: john.doe@microsoft.com
Event Timestamp: 2024-04-26T12:34:56Z
Level: Information
Status: Succeeded
Operation Name: Update Role Assignment

Due to our limited access, we are unable to see specifically which changes were made aside from the actions listed under the operation name in the results provided.

Regards,


```

## Troubleshooting

- **Authentication Issues**: Ensure you're logged into Azure CLI and have active subscriptions with proper permissions.
- **Command Errors**: If Azure CLI commands fail, check for typos in subscription names, user IDs, and ensure dates are correctly formatted.

---

