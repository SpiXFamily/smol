import unittest
import os

class TestIniFile(unittest.TestCase):
    def test_ini_file_exists(self):
        folder_path = 'ini'
        ini_file_name = 'config.ini'
        ini_file_path = os.path.join(folder_path, ini_file_name)
    #def test_ini_file_exists(self):
    #    folder_path = '../ini'
    #    ini_file_name = 'mail.ini'
    #    ini_file_path = os.path.join(folder_path, ini_file_name)

        
        self.assertTrue(os.path.isfile(ini_file_path), f"INI file '{ini_file_name}' does not exist in folder '{folder_path}'")

if __name__ == '__main__':
    unittest.main()

