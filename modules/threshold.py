import os
import configparser

def read_ini():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"ini/config.ini")
    
    try:
        config.read(config_path)
        thresholds = {
            'ram_threshold': int(config.get("Thresholds", "ram_threshold")),
            'critical_ram_threshold': int(config.get("Thresholds", "critical_ram_threshold")),
            'disk_threshold': int(config.get("Thresholds", "disk_threshold")),
            'critical_disk_threshold': int(config.get("Thresholds", "critical_disk_threshold")),
            'interval': int(config.get("Thresholds", "interval"))
        }
        return thresholds
    except configparser.Error as e:
        print(f"Error reading configuration file: {e}")
        return None
def usage_interval():
    interval = read_ini()
    interval = thresholds['interval']
    return interval
# Example usage:
thresholds = read_ini()
if thresholds:
    print(thresholds['ram_threshold'])
    print(thresholds['disk_threshold'])
    print(thresholds['critical_ram_threshold'])
    print(thresholds['critical_disk_threshold'])
    print(thresholds['interval'])

def threshold_ram(ram_percentage, ram_threshold = thresholds["ram_threshold"], critical_ram_threshold = thresholds["critical_ram_threshold"]):
    ram_threshold = read_ini()
    critical_ram_threshold = read_ini()
    ram_threshold = thresholds["ram_threshold"]
    critical_ram_threshold = thresholds["critical_ram_threshold"]
    if ram_percentage >= critical_ram_threshold:
        return True
    elif ram_percentage >= ram_threshold:
        return False
    else:
        pass

def threshold_disk(disk_percentage, disk_threshold = thresholds["disk_threshold"], critical_disk_threshold = thresholds["critical_disk_threshold"]):
    disk_threshold = read_ini()
    critical_disk_threshold = read_ini()
    disk_threshold = thresholds["disk_threshold"]
    critical_disk_threshold = thresholds["critical_disk_threshold"]
    if disk_percentage >= critical_disk_threshold:
        return True
    elif disk_percentage >= disk_threshold:
        return False
    else:
        pass