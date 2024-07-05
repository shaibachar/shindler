import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import shutil
import sys

# Add the src directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import file_copy_script as script

class TestFileCopyScript(unittest.TestCase):

    def setUp(self):
        self.file_list_json = {
            "files": [
                {"filename": "a.txt", "description": "desc1", "tags": ["tag1"]},
                {"filename": "b.txt", "description": "desc2", "tags": ["tag2"]}
            ]
        }
        self.file_list_path = "file_list.json"
        self.source_folder = "source"
        self.destination_folder = "destination"
        self.history_file = "history.json"
    
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"file_list": [], "source_folder": [], "destination_folder": []}))
    @patch("os.path.exists", return_value=True)
    def test_load_history(self, mock_exists, mock_open):
        history = script.load_history()
        self.assertEqual(history, {"file_list": [], "source_folder": [], "destination_folder": []})
    
    @patch("builtins.open", new_callable=mock_open)
    def test_save_history(self, mock_open):
        script.save_history(["file1"], ["folder1"], ["folder2"])
        mock_open.assert_called_once_with("history.json", "w")
        handle = mock_open()
        handle.write.assert_called_once_with(json.dumps({"file_list": ["file1"], "source_folder": ["folder1"], "destination_folder": ["folder2"]}, indent=4))

    @patch("os.path.exists", side_effect=lambda x: x == "file_list.json")
    def test_load_file_list(self, mock_exists):
        with patch("builtins.open", mock_open(read_data=json.dumps(self.file_list_json))):
            num_files = script.load_file_list(self.file_list_path)
        self.assertEqual(num_files, 2)

    @patch("os.path.exists", return_value=True)
    def test_validate_files(self, mock_exists):
        missing_files = script.validate_files(self.file_list_json["files"], self.destination_folder)
        self.assertEqual(missing_files, [])

    @patch("os.makedirs")
    @patch("os.path.exists", side_effect=lambda x: x in ["file_list.json", "source_folder", os.path.join("source_folder", "example1.txt")])
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"files": [{"filename": "a.txt"}, {"filename": "b.txt"}]}))
    @patch("shutil.copy2")
    def test_copy_files(self, mock_copy2, mock_open, mock_exists, mock_makedirs):
        copied_files_count, missing_files = script.copy_files(self.file_list_path, self.source_folder, self.destination_folder)
        self.assertEqual(copied_files_count, 1)
        self.assertEqual(missing_files, ["b.txt"])
    
    @patch("os.path.exists", side_effect=lambda x: x in ["file_list.json", "destination_folder"])
    def test_validate_destination(self, mock_exists):
        with patch("builtins.open", mock_open(read_data=json.dumps(self.file_list_json))):
            missing_files = script.validate_destination(self.file_list_path, self.destination_folder)
        self.assertEqual(missing_files, ["a.txt", "b.txt"])

if __name__ == "__main__":
    unittest.main()
