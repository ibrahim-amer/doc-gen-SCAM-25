import unittest
from unittest.mock import MagicMock, patch
from tinaa.doc_gen.config.BaseLLM import BaseLLM
from tinaa.doc_gen.config.config import Config
from tinaa.doc_gen.parsing.treesitter import ParseFile
from tinaa.doc_gen.config.LLMFactory import LLMFactory

# Dummy Node class for mocking Tree-sitter nodes
class DummyNode:
    def __init__(self, type_, children=None, parent=None, prev_sibling=None, start_byte=0, end_byte=0, text=b''):
        self.type = type_
        self.children = children or []
        self.parent = parent
        self.prev_sibling = prev_sibling
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.text = text

    def child(self, idx):
        if idx < len(self.children):
            return self.children[idx]
        return None

    @property
    def child_count(self):
        return len(self.children)

    def child_by_field_name(self, name):
        if name == 'body':
            for c in self.children:
                if c.type == 'body':
                    return c
            return None
        if name == 'name':
            for c in self.children:
                if c.type == 'identifier':
                    return c
            return None
        return None

class DummyTree:
    def __init__(self, root_node):
        self.root_node = root_node

class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.config = Config.load_from_file()
        self.llm = LLMFactory.from_config(self.config, self.config.provider_enum)
        self.parser = ParseFile(llm_model=self.llm)

    def test_get_indentation_level(self):
        code = "def foo():\n    pass\n"
        start_byte = code.index('pass')
        indent = self.parser.get_indentation_level(code, start_byte)
        self.assertEqual(indent, 4)

        indent0 = self.parser.get_indentation_level(code, 0)
        self.assertEqual(indent0, 0)

    def test_has_docstring_or_comment_numpydoc(self):
        string_node = DummyNode('string')
        expr_stmt = DummyNode('expression_statement', children=[string_node])
        body_node = DummyNode('body', children=[expr_stmt])
        func_node = DummyNode('function_definition', children=[body_node])

        self.assertTrue(self.parser.has_docstring_or_comment(func_node, 'numpydoc'))

        non_string_node = DummyNode('identifier')
        expr_stmt2 = DummyNode('expression_statement', children=[non_string_node])
        body_node2 = DummyNode('body', children=[expr_stmt2])
        func_node2 = DummyNode('function_definition', children=[body_node2])

        self.assertFalse(self.parser.has_docstring_or_comment(func_node2, 'numpydoc'))

    def test_has_docstring_or_comment_tsdoc_with_comment(self):
        comment_node = DummyNode('comment')
        node = DummyNode('function_declaration', prev_sibling=comment_node)
        self.assertTrue(self.parser.has_docstring_or_comment(node, 'tsdoc'))

    def test_has_docstring_or_comment_tsdoc_without_comment(self):
        node = DummyNode('function_declaration')
        self.assertFalse(self.parser.has_docstring_or_comment(node, 'tsdoc'))

    def test_has_docstring_or_comment_other_with_comment(self):
        comment_node = DummyNode('comment')
        node = DummyNode('function_declaration', prev_sibling=comment_node)
        self.assertTrue(self.parser.has_docstring_or_comment(node, 'other'))

    def test_has_docstring_or_comment_other_without_comment(self):
        node = DummyNode('function_declaration')
        self.assertFalse(self.parser.has_docstring_or_comment(node, 'other'))
    
    @patch('tinaa.doc_gen.parsing.treesitter.CallModel')
    @patch('tinaa.doc_gen.parsing.treesitter.Helpers')
    @patch('tinaa.doc_gen.parsing.treesitter.get_language')
    @patch('tinaa.doc_gen.parsing.treesitter.Parser')
    def test_check_file_with_existing_docstring(self, mock_parser_cls, mock_get_language, mock_helpers_cls, mock_callmodel_cls):
        # Setup mocks similar to above
        mock_language = MagicMock()
        mock_get_language.return_value = mock_language
        
        mock_parser = MagicMock()
        mock_parser_cls.return_value = mock_parser
        
        root_node = DummyNode('root', children=[])
        identifier_node = DummyNode('identifier', text=b"foo")
        func_node = DummyNode('function_definition', children=[identifier_node])
        root_node.children.append(func_node)
        
        dummy_tree = DummyTree(root_node)
        mock_parser.parse.return_value = dummy_tree
        
        func_node.child_by_field_name = MagicMock(return_value=identifier_node)
        
        # Patch has_docstring_or_comment to return True (simulate existing docstring)
        self.parser.has_docstring_or_comment = MagicMock(return_value=True)
        
        language_info = {
            'elements_to_document': ['function_definition'],
            'doc_format': 'numpydoc',
            'language': 'python'
        }
        
        code = "def foo():\n    pass\n"
        
        modified_code = self.parser.check_file(code, unicorn=True, language_info=language_info, debug=False)
        
        # Since docstring exists, no insertion should be done, output should be original code
        self.assertEqual(modified_code, code)
    @patch('tinaa.doc_gen.parsing.treesitter.CallModel')
    @patch('tinaa.doc_gen.parsing.treesitter.Helpers')
    def test_add_docstring_positive_case(self, mock_helpers_cls, mock_callmodel_cls):
        global elements_to_document, doc_type, language, unicorn, modified_code, insertions

        # Setup globals
        elements_to_document = ["function_definition"]
        doc_type = "numpydoc"
        language = "python"
        unicorn = True
        modified_code = "def foo():\n    pass\n"
        insertions = []

        # Setup mocks
        mock_callmodel = MagicMock()
        mock_callmodel.insert_docstring.return_value = "Generated docstring"
        mock_callmodel_cls.return_value = mock_callmodel

        mock_helpers = MagicMock()
        mock_helpers.indent_docstring.side_effect = lambda text, indent: [f"{' ' * indent}{line}" for line in text.split('\n')]
        mock_helpers_cls.return_value = mock_helpers
if __name__ == "__main__":
    unittest.main()
