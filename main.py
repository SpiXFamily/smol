#!/usr/bin/env python3
import time
import os
import threading
import json
import sys
import socket
sys.path.append('modules')
from loggingmodule import get_logged_in_users, get_directory, get_monitoring_info, get_system_info, write_to_logfile, ram_data, disk_data
from mailmodule import send_warning_email, monitoring_mail, monitoring_password, admin_mail
from flask import Flask, render_template, jsonify
from threshold import threshold_ram, threshold_disk, usage_interval

#import unittest

directory_path = "logs"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print("Folder created successfully.")
else:
    print("Folder already exists.")
logfile_path = "logs/logfile.log"
user_logfile_path = "logs/user_logfile.log"
app = Flask(__name__)
# -------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logging_interval')
def logging_interval():
    interval = usage_interval()
    interval = interval * 1000
    return jsonify({'interval': int(interval)})

@app.route('/get_initial_data')
def get_initial_data():
    try:
        with open('ini/data.json', 'r') as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stored_data = {'ram_info': [], 'disk_info': []}

    return jsonify(stored_data)


@app.route('/get_data')
def get_data():
    try:
        # Load existing data from file
        with open('ini/data.json', 'r') as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data from file: {e}")
        stored_data = {'ram_info': [], 'disk_info': []}

    # Get current monitoring data with timestamp
    timestamp = int(time.time())
    
    # Get RAM and Disk data
    ram_info = {
        'timestamp': timestamp,
        'percent': ram_data()  # Modify ram_data function to return percentage
    }

    disk_info = {
        'timestamp': timestamp,
        'percent': disk_data()  # Modify disk_data function to return percentage
    }
    # Update stored data with current data
    stored_data['ram_info'].append(ram_info)
    stored_data['disk_info'].append(disk_info)
    # Limit the stored data to the last 100 entries
    stored_data['ram_info'] = stored_data['ram_info'][-20:]
    stored_data['disk_info'] = stored_data['disk_info'][-20:]
    try:
        # Save the updated data back to the file
        with open('ini/data.json', 'w') as file:
            json.dump(stored_data, file)
    except Exception as e:
        print(f"Error saving data to file: {e}")
    return jsonify({'ram_info': ram_info, 'disk_info': disk_info})

# Start monitoring to use in threading
def start_monitoring():
    main()
# Main function to use all modules
def main():
    try:
        while True:
                # Get user Logins and write to logfile
                user_logins = get_logged_in_users()
                write_to_logfile(user_logfile_path, user_logins)
                # Get monitoring information and write to logfile
                monitoring_info = get_monitoring_info()
                write_to_logfile(logfile_path, monitoring_info)
                print(user_logins)
                print(monitoring_info)
                # Check if Threshold has been reached and send mail if necessary
                device_name = socket.gethostname()
                print(device_name)
    # EMAIL DISABLED UNTIL USED! TO PREVENT SPAM-FLOODING IN CASE OF ERRORS
    
                # if threshold_ram(ram_data()) == True:
                #     subject = f'[CRITICAL!] RAM HAS REACHED {ram_data()}% !!!'
                #     message_body = f'Your RAM of the device {device_name} with the logged in users: \n{user_logins}\nhas reached a critical state.\n\n {get_system_info()}'
                #     send_warning_email(monitoring_mail, monitoring_password, admin_mail, subject, message_body)
                # elif threshold_ram(ram_data()) == False:
                #     subject = f'[WARNING!] RAM HAS REACHED {ram_data()}% !!!'
                #     message_body = f'Your RAM of the device {device_name} with the logged in users\n{user_logins}\nhas reached a warning state.\n\n {get_system_info()}'
                #     send_warning_email(monitoring_mail, monitoring_password, admin_mail, subject, message_body)                    
                # else:
                #     pass
                # if threshold_disk(disk_data()) == True:
                #     subject = f'[WARNING!]DISK SPACE HAS REACHED {disk_data()}% !!!'
                #     message_body = f'Your Disk Space of the device {device_name} with the logged in users\n{user_logins}\nhas reached a warning state.\n\n {get_system_info()}'
                #     send_warning_email(monitoring_mail, monitoring_password, admin_mail, subject, message_body)   
                # elif threshold_disk(disk_data()) == False:
                #     subject = f'[CRITICAL!]DISK SPACE HAS REACHED {disk_data()}% !!!'
                #     message_body = f'Your Disk Space of the device {device_name} with the logged in users\n{user_logins}\nhas reached a critical state.\n\n {get_system_info()}'
                #     send_warning_email(monitoring_mail, monitoring_password, admin_mail, subject, message_body)   
                # else:
                #     pass
                time.sleep(usage_interval())

    except:
        print("An error in the Main function occured...")

if __name__ == '__main__':
    # Print system info into terminal when started
    system_info = get_system_info()
    print(system_info)
    get_directory()
    time.sleep(1)
    monitoring_thread = threading.Thread(target=start_monitoring)
    monitoring_thread.start()
    app.run(debug=False)

    
