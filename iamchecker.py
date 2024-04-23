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

def get_iam_write_activity_events(start_time, end_time):
    command = (
        f"az monitor activity-log list "
        f"--start-time {start_time} "
        f"--end-time {end_time} "
        f"--max-events 5000 "
        f"--query \"[?contains(operationName.localizedValue, 'role')].[{{Caller_name:caller, EventTimestamp:eventTimestamp, Level:level, Status:status.value, OperationName:operationName.localizedValue}}]\" "
        f"--output json"
    )
    output = run_az_command(command)
    if output:
        return json.loads(output)
    return None

def display_events(events):
    if not events:
        print("No IAM write activity events found for the specified date.")
        return
    
    for event_list in events:
        if isinstance(event_list, list):
            for event in event_list:
                if isinstance(event, dict):
                    print(f"Caller Name: {event.get('Caller_name', 'N/A')}")
                    print(f"Event Timestamp: {event.get('EventTimestamp', 'N/A')}")
                    print(f"Level: {event.get('Level', 'N/A')}")
                    print(f"Status: {event.get('Status', 'N/A')}")
                    print(f"Operation Name: {event.get('OperationName', 'N/A')}\n")
                else:
                    print("Unexpected data format encountered in nested event: ", event)
        else:
            print("Unexpected data format encountered in event list: ", event_list)
 
def main():
    set_cloud_type()
    set_subscription()
    start_time, end_time = get_date_from_user()
    if start_time and end_time:
        events = get_iam_write_activity_events(start_time, end_time)
        display_events(events)
    else:
        print("Invalid date entered. Exiting.")

if __name__ == "__main__":
    main()
