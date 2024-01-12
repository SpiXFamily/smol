import psutil
from datetime import datetime
import os
import platform
import socket


def ram_data():
    information = psutil.virtual_memory()
    information = information.percent
    return information
def disk_data():
    information = psutil.disk_usage('/')
    information = information.percent
    return information

# Get the logged in users on the server/device
def get_logged_in_users():
    users = psutil.users()
    logged_in_users = [(user.name, user.terminal, user.host, user.started) for user in users]
    return logged_in_users
# Get the current working directory
def get_directory():
    directory = os.getcwd()
    print("The current directory is:", directory) 
# Get the RAM and DISK information of the server/device
def get_monitoring_info():
    ram_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    monitoring_info = (
        f"---------------------------\n"
        f"Timestamp: {datetime.now()}\n\n"
        f"RAM INFO:\n"
        f"Total RAM: {ram_info.total / (1024 ** 3):.2f} GB\n"
        f"Available RAM: {ram_info.available / (1024 ** 3):.2f} GB\n"
        f"RAM Usage: {ram_info.percent}%\n\n"
        f"DISK INFO:\n"
        f"Total Disk Space: {disk_info.total / (1024 ** 3):.2f} GB\n"
        f"Free Disk Space: {disk_info.free / (1024 ** 3):.2f} GB\n"
        f"Available Disk Space: {disk_info.percent}%\n\n"
        f"---------------------------"
    )
    return monitoring_info
# Get basic system information of the server/device
def get_system_info():
    username = os.getlogin()
    current_directory = os.getcwd()
    os_info = f"Betriebssystem: {platform.system()} {platform.version()}"  
    python_version = f"Python-Version: {platform.python_version()}"
    processor_info = f"Prozessor: {platform.processor()}"
    ip_address = f"IP-Adresse: {socket.gethostbyname(socket.gethostname())}"
    system_info = (
        f"Timestamp: {datetime.now()}\n"
        f"Benutzername: {username}\n"
        f"Aktuelles Dateiverzeichnis: {current_directory}\n"
        f"{os_info}\n"
        f"{python_version}\n"
        f"{processor_info}\n"
        f"{ip_address}\n\n"
    )
    return system_info
# Write Monitoring information the the logfiles
def write_to_logfile(logfile_path, monitoring_info):
    with open(logfile_path, 'a') as log_file:
        try:
            if isinstance(monitoring_info, list):
                username, terminal, host, started = monitoring_info[0]
                log_entry = (
                    f"Username: {username}, "
                    f"Terminal: {terminal if terminal else 'N/A'}, "
                    f"Host: {host if host else 'N/A'}, "
                    f"Started: {datetime.fromtimestamp(started).strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"Time-Now: {datetime.now()}"
                )
                log_file.write(log_entry + '\n')
            elif isinstance(monitoring_info, str):
                log_file.write(monitoring_info)
            else:
                raise ValueError("Unsupported type for monitoring_info")
        except Exception as e:
            print(f"Error writing to logfile: {e}")
