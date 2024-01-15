import unittest
import importlib
import sys
sys.path.append('modules')
class TestMainFile(unittest.TestCase):
    def test_all_modules_correct(self):
        # List of module names to validate
        module_names = ['loggingmodule', 'mailmodule', 'threshold']
        
        for module_name in module_names:
            try:
                importlib.import_module(module_name)
            except ImportError:
                self.fail(f"Module '{module_name}' not found or contains errors")

if __name__ == '__main__':
    unittest.main()

