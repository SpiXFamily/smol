import unittest
import os

class TestIniFile(unittest.TestCase):
    def test_ini_file_exists(self):
        folder_path = 'templates'
        ini_file_name = 'index.html'
        ini_file_path = os.path.join(folder_path, ini_file_name)

if __name__ == '__main__':
    unittest.main()

