import unittest
import json

class TestJsonFile(unittest.TestCase):
    def test_read_json_file(self):
        file_path = "../ini/data.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        self.assertIsNotNone(data)
        # Add more assertions or tests based on your requirements

if __name__ == "__main__":
    unittest.main()
