import os

def check_log_files(../logs/logfile.log):
    for log_file_path in log_file_paths:
        if os.path.isfile(log_file_path):
            print(f"Log file '{log_file_path}' exists.")
        else:
            print(f"Log file '{log_file_path}' does not exist.")

log_files = ["path/to/logfile1.log", "path/to/logfile2.log"]
check_log_files(log_files)
