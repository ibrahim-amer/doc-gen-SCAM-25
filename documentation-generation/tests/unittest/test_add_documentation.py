import unittest
from unittest.mock import patch, mock_open, MagicMock
from tinaa.doc_gen.add_documentation import Main
import os
import json

class TestMain(unittest.TestCase):
    def setUp(self):
        self.main = Main()
        self.sample_json = {
            "languages": [
                {
                    "name": "Python",
                    "parser": "Arpeggio",
                    "doc_format": "Google",
                    "extensions": [".py"],
                    "elements_to_document": ["functions", "classes"]
                },
                {
                    "name": "Java",
                    "parser": "TreeSitter",
                    "doc_format": "Javadoc",
                    "extensions": [".java"],
                    "elements_to_document": ["methods", "classes"]
                }
            ]
        }

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_get_language_info_python(self, mock_json_load, mock_file):
        mock_json_load.return_value = self.sample_json
        with patch("os.path.dirname", return_value="/fake_dir"):
            info, should_document = self.main.get_language_info("test.py")

        self.assertTrue(should_document)
        self.assertEqual(info["language"], "python")
        self.assertEqual(info["parser"], "arpeggio")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_get_language_info_unknown_ext(self, mock_json_load, mock_file):
        mock_json_load.return_value = self.sample_json
        with patch("os.path.dirname", return_value="/fake_dir"):
            info, should_document = self.main.get_language_info("file.unknown")
        
        self.assertFalse(should_document)
        self.assertEqual(info, {})

    @patch("tinaa.doc_gen.parsing.arpeg.Arpeg.check_file")
    @patch("builtins.open", new_callable=mock_open, read_data="def foo(): pass")
    @patch("tinaa.doc_gen.add_documentation.Main.get_language_info")
    def test_process_file_arpeggio(self, mock_get_lang_info, mock_file_open, mock_check_file):
        mock_get_lang_info.return_value = ({
            "parser": "arpeggio",
            "doc_format": "google",
            "language": "python",
            "extensions": [".py"]
        }, True)
        mock_check_file.return_value = '"""Docstring"""\ndef foo(): pass'

        test_file_path = "/tmp/fake.py"
        self.main.process_file(test_file_path, "fake.py", unicorn=True)

        mock_file_open.assert_called_with(test_file_path, "w")
        mock_check_file.assert_called_once()

    @patch("tinaa.doc_gen.parsing.treesitter.ParseFile.check_file")
    @patch("builtins.open", new_callable=mock_open, read_data="public void foo() {}")
    @patch("tinaa.doc_gen.add_documentation.Main.get_language_info")
    def test_process_file_treesitter(self, mock_get_lang_info, mock_file_open, mock_check_file):
        mock_get_lang_info.return_value = ({
            "parser": "treesitter",
            "doc_format": "javadoc",
            "language": "java",
            "extensions": [".java"],
            "elements_to_document": ["methods", "classes"]
        }, True)
        mock_check_file.return_value = "/** Javadoc */\npublic void foo() {}"

        test_file_path = "/tmp/fake.java"
        self.main.process_file(test_file_path, "fake.java", unicorn=False)

        mock_file_open.assert_called_with(test_file_path, "w")
        mock_check_file.assert_called_once()

    def test_process_file_none_path(self):
        with patch("builtins.print") as mock_print:
            self.main.process_file(None, "file.py", unicorn=True)
            mock_print.assert_called_with("No file path provided.")

if __name__ == "__main__":
    unittest.main()
