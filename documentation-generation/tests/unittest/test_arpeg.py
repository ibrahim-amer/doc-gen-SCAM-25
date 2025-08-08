import unittest
from unittest.mock import patch, MagicMock
from tinaa.doc_gen.parsing.arpeg import Arpeg, Visitor, block, statemachine, art_capsule
from arpeggio import visit_parse_tree, ParserPython

class TestArpegDocstringDetection(unittest.TestCase):

    def setUp(self):
        self.arpeg = Arpeg()

    def test_artdoc_detected(self):
        lines = [
            "    /**",
            "    * This is a comment",
            "    */",
            "    state Foo {",
            "        port bar: Bar;",
            "    }",

        ]
        result = self.arpeg.has_docstring("artdoc", lines, 4)
        self.assertTrue(result)

    def test_artdoc_not_detected(self):
        lines = [
            "    // no artdoc here",
            "    capsule Foo {",
            "        port bar: Bar;",
            "    }",
        ]
        result = self.arpeg.has_docstring("artdoc", lines, 2)
        self.assertFalse(result)

    def test_hashcomment_detected(self):
        lines = [
            "# This is a comment",
            "def my_function():",
            "    pass",
        ]
        result = self.arpeg.has_docstring("hashcomment", lines, 2)
        self.assertTrue(result)

    def test_hashcomment_not_detected(self):
        lines = [
            "def my_function():",
            "    pass",
        ]
        result = self.arpeg.has_docstring("hashcomment", lines, 2)
        self.assertFalse(result)

    @patch("tinaa.doc_gen.parsing.arpeg.ParserPython")
    @patch("tinaa.doc_gen.parsing.arpeg.visit_parse_tree", return_value=None)
    def test_check_file_no_positions(self, mock_visit_tree, mock_parser_class):
        code = "capsule Foo {\n    port bar: Bar;\n}"
        language_info = {"language": "art", "doc_format": "artdoc"}

        global positions
        positions = []  

        mock_parser = MagicMock()
        mock_parser.parse.return_value = "tree"
        mock_parser_class.return_value = mock_parser

        result = self.arpeg.check_file(code, unicorn=False, language_info=language_info)
        self.assertEqual(result, code)
if __name__ == "__main__":
    unittest.main()
