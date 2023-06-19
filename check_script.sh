#!/bin/bash

# Function to check if the Python script is running
is_script_running() {
    ps aux | grep "python click.py" | grep -v grep
}

# Loop to check and re-run the script every 30 minutes
while true; do
    # Check if the script is running
    if ! is_script_running; then
        echo "Script is not running. Re-running..."
        # Run the Python script using nohup and redirect output to nohup.out
        nohup python click.py > nohup.out 2>&1 &
    fi

    # Delay for 30 minutes (30 minutes = 1800 seconds)
    sleep 1800
done
