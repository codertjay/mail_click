#!/bin/bash

# Function to check if the Python script is running
is_script_running() {
    ps aux | grep "python3 _click.py" | grep -v grep
}

# Activate the virtual environment
source /home/ubuntu/mail_click/venv/bin/activate

# Check if the script is running
if ! is_script_running; then
    echo "Script is not running. Re-running..."
    # Run the Python script using nohup and redirect output to nohup.out
    nohup /home/ubuntu/mail_click/venv/bin/python3 /home/ubuntu/mail_click/_click.py > /home/ubuntu/mail_click/nohup.log 2>&1 &
fi
