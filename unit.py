import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime
import sys
import os
import psutil
sys.path.append('modules')
from loggingmodule import ram_data, disk_data, get_logged_in_users, get_monitoring_info, get_system_info, write_to_logfile

class TestMonitoringModule(unittest.TestCase):

    def test_ram_data(self):
        # Mocking psutil.virtual_memory().percent
        with patch('psutil.virtual_memory') as mock_virtual_memory:
            mock_virtual_memory.return_value.percent = 75
            result = ram_data()
            self.assertEqual(result, 75)

    def test_disk_data(self):
        # Mocking psutil.disk_usage('/').percent
        with patch('psutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value.percent = 50
            result = disk_data()
            self.assertEqual(result, 50)

    def test_get_logged_in_users(self):
        # Mocking psutil.users()
        with patch('psutil.users') as mock_users:
            mock_users.return_value = [psutil._common.snamedtuple('suser', ['name', 'terminal', 'host', 'started'], 'suser')('user1', 'pts/0', 'localhost', 1631871100)]
            result = get_logged_in_users()
            self.assertEqual(result, [('user1', 'pts/0', 'localhost', 1631871100)])

    def test_get_monitoring_info(self):
        # Mocking psutil.virtual_memory(), psutil.disk_usage()
        with patch('psutil.virtual_memory') as mock_virtual_memory, patch('psutil.disk_usage') as mock_disk_usage:
            mock_virtual_memory.return_value.total = 1024 ** 3
            mock_virtual_memory.return_value.available = 512 ** 3
            mock_virtual_memory.return_value.percent = 60
            mock_disk_usage.return_value.total = 2048 ** 3
            mock_disk_usage.return_value.free = 1024 ** 3
            mock_disk_usage.return_value.percent = 30

            result = get_monitoring_info()
            expected_result = (
                "---------------------------\n"
                "Timestamp: {}\n\n"
                "RAM INFO:\n"
                "Total RAM: 1.00 GB\n"
                "Available RAM: 0.50 GB\n"
                "RAM Usage: 60%\n\n"
                "DISK INFO:\n"
                "Total Disk Space: 2.00 GB\n"
                "Free Disk Space: 1.00 GB\n"
                "Available Disk Space: 30%\n\n"
                "---------------------------"
            )
            self.assertEqual(result, expected_result)

    def test_get_system_info(self):
        # Mocking os.getlogin(), os.getcwd(), platform.system(), platform.version(), platform.python_version(), platform.processor(), socket.gethostbyname(socket.gethostname())
        with patch('os.getlogin') as mock_getlogin, patch('os.getcwd') as mock_getcwd, patch('platform.system') as mock_system, patch('platform.version') as mock_version, patch('platform.python_version') as mock_python_version, patch('platform.processor') as mock_processor, patch('socket.gethostbyname') as mock_gethostbyname:
            mock_getlogin.return_value = 'test_user'
            mock_getcwd.return_value = '/test/directory'
            mock_system.return_value = 'Linux'
            mock_version.return_value = '4.15.0-123-generic'
            mock_python_version.return_value = '3.8.10'
            mock_processor.return_value = 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz'
            mock_gethostbyname.return_value = '192.168.1.1'

            result = get_system_info()
            expected_result = (
                "Timestamp: {}\n"
                "Benutzername: test_user\n"
                "Aktuelles Dateiverzeichnis: /test/directory\n"
                "Betriebssystem: Linux 4.15.0-123-generic\n"
                "Python-Version: 3.8.10\n"
                "Prozessor: Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz\n"
                "IP-Adresse: 192.168.1.1\n\n".format(datetime.now())
            )
            self.assertEqual(result, expected_result)

    def test_write_to_logfile(self):
        # Mocking open() and checking if the correct content is written
        with patch('builtins.open', create=True) as mock_open:
            fake_file = StringIO()
            mock_open.return_value = fake_file
            monitoring_info = "Test Monitoring Info"
            write_to_logfile('/DELETE_JUST_TESTING/logfile/path.log', monitoring_info)
            self.assertEqual(fake_file.getvalue(), monitoring_info + '\n')

if __name__ == '__main__':
    unittest.main()
