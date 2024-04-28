"""
Script Name: iamchecker.py
Author: michael.quintero@rackspace.com
Description: This script will search for IAM related events based on the account input the user provides
Pre-Requisites: Python 3, AZ Cli, Global Admin privileges
Usage: iamchecker.py (Will present user with questions)
"""

import json
import subprocess
from datetime import datetime, timedelta

def run_az_command(command):
    try:
        process = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing Azure CLI command: {e}")
        return None

def set_cloud_type():
    cloud_type = input("Enter the cloud type (either AzureCloud or AzureUSGovernment): ")
    command = f"az cloud set --name {cloud_type}"
    run_az_command(command)

def set_subscription():
    subscription_name = input("Enter the subscription name or ID: ")
    command = f"az account set --subscription {subscription_name}"
    run_az_command(command)
    return subscription_name  # Return the subscription name to the caller

def get_date_from_user():
    date_str = input("Enter the date to search for (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_time = date
        end_time = start_time + timedelta(days=1)
        return start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None, None

def get_user_input():
    username_or_guid = input("Enter the Username or GUID to search for (leave blank to include all): ")
    return username_or_guid

def get_status_input():
    valid_statuses = ["Failed", "Started", "Succeeded"]
    status_input = input(f"Enter the status to filter by ({', '.join(valid_statuses)}), or leave blank for all: ")
    if status_input in valid_statuses:
        return status_input
    return None

def get_iam_write_activity_events(start_time, end_time, username_or_guid, status):
    user_filter = f" && caller == '{username_or_guid}'" if username_or_guid else ""
    status_filter = f" && status.value == '{status}'" if status else ""
    
    command = (
        f"az monitor activity-log list "
        f"--start-time {start_time} "
        f"--end-time {end_time} "
        f"--max-events 5000 "
        f"--query \"[?contains(operationName.localizedValue, 'role') {user_filter} {status_filter}].[{{Caller_name:caller, EventTimestamp:eventTimestamp, Level:level, Status:status.value, OperationName:operationName.localizedValue}}]\" "
        f"--output json"
    )
    output = run_az_command(command)
    if output:
        return json.loads(output)
    return None

def display_events(events, subscription_name, username_or_guid):
    if not events:
        print("No IAM write activity events found for the specified date.")
        return
    
    user_provided = "NO USER PROVIDED" if not username_or_guid else username_or_guid
    print(f"Hello,\n\nThe user '{user_provided}' made the following IAM updates on the '{subscription_name}' donated subscription:\n")

    if events and isinstance(events[0], list):
        # Flatten the list if it's a list of lists
        events = [item for sublist in events for item in sublist]
    
    for event in events:
        if isinstance(event, dict):
            print(f"Caller Name: {event.get('Caller_name', 'N/A')}")
            print(f"Event Timestamp: {event.get('EventTimestamp', 'N/A')}")
            print(f"Level: {event.get('Level', 'N/A')}")
            print(f"Status: {event.get('Status', 'N/A')}")
            print(f"Operation Name: {event.get('OperationName', 'N/A')}\n")
        else:
            print("Unexpected data format encountered in event: ", event)
    
    print("Due to our limited access, we are unable to see specifically which changes were made aside from the actions listed under the operation name in the results provided.\n\nRegards,\n\nMike Quintero\nCloud Engineer II\nPCM DIR-OPS\nRackspace Technology")


def main():
    set_cloud_type()
    subscription_name = set_subscription()
    start_time, end_time = get_date_from_user()
    username_or_guid = get_user_input()
    status = get_status_input()
    if start_time and end_time:
        events = get_iam_write_activity_events(start_time, end_time, username_or_guid, status)
        display_events(events, subscription_name, username_or_guid)
    else:
        print("Invalid date entered. Exiting.")

if __name__ == "__main__":
    main()
