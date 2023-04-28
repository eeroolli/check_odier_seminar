#!/bin/bash

# Activate the virtual environment
source /path/to/venv/bin/activate ds

# Change to the directory containing the Python script
cd /home/eero_ds/dataanalyst/check_odier_seminar/

# Run the Python continuously script in the background. 
# nohup python check_odiers_website.py > /dev/null 2>&1 &

# Run the Python script with a cron job takes less resources.
python check_odiers_website.py
