import os
import tempfile
import unittest
from tinaa.doc_gen.helpers import Helpers  


class DummyChild:
    def __init__(self, type_):
        self.type = type_


class DummyNode:
    def __init__(self, children):
        self.children = children


class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.helpers = Helpers()

    def test_add_makehelp_rules_adds_when_missing(self):
        input_code = "all:\n\techo Hello"
        result = self.helpers.add_makehelp_rules(input_code)
        self.assertIn(".PHONY: help", result)
        self.assertIn("help:", result)

    def test_add_makehelp_rules_does_not_add_when_present(self):
        input_code = ".PHONY: help\nsome_other_rule:\n\techo World"
        result = self.helpers.add_makehelp_rules(input_code)
        # Should not add duplicate help rules
        self.assertEqual(result.count(".PHONY: help"), 1)

    def test_make_file_find_comment_child_returns_true_if_found(self):
        node = DummyNode([DummyChild("comment"), DummyChild("other")])
        self.assertTrue(self.helpers.make_file_find_comment_child(node, "comment"))

    def test_make_file_find_comment_child_returns_false_if_not_found(self):
        node = DummyNode([DummyChild("not_comment"), DummyChild("other")])
        self.assertFalse(self.helpers.make_file_find_comment_child(node, "comment"))

    def test_indent_docstring_indents_all_lines_correctly(self):
        docstring = "Line one\nLine two\nLine three"
        indent_level = 2
        indented = self.helpers.indent_docstring(docstring, indent_level)
        expected_indent = ' ' * (indent_level + 4)
        for line in indented:
            self.assertTrue(line.startswith(expected_indent))
        self.assertEqual(len(indented), 3)
        # Original lines should appear in order after indentation
        for i, line in enumerate(indented):
            self.assertIn(docstring.split('\n')[i], line)

    def test_read_jinja_template_renders_correctly(self):
        template_content = "Hello {{ name }}!"
        data = {"name": "Tester"}

        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
            tmp.write(template_content)
            tmp_path = tmp.name

        try:
            rendered = self.helpers.read_jinja_template(tmp_path, data)
            self.assertEqual(rendered, "Hello Tester!")
        finally:
            os.remove(tmp_path)

    def test_read_jinja_template_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.helpers.read_jinja_template("non_existent_template.j2", {})


if __name__ == "__main__":
    unittest.main()
