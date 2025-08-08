import unittest
from tinaa.doc_gen.few_shot_examples import FewShotExamples

class TestFewShotExamples(unittest.TestCase):

    def setUp(self):
        self.few_shot_examples = FewShotExamples()

    def test_function_examples(self):
        docstrings, code = self.few_shot_examples.examples("function")
        self.assertEqual(len(docstrings), 3)
        self.assertEqual(len(code), 3)
        self.assertIn("bubble_sort", code[0]) # Check for a keyword in the code
        self.assertIn("Sorts an array", docstrings[0]["description"]) # Check description

    def test_class_examples(self):
        docstrings, code = self.few_shot_examples.examples("class")
        self.assertEqual(len(docstrings), 3)
        self.assertEqual(len(code), 3)
        self.assertIn("class Person:", code[0])
        self.assertIn("A class to represent a person", docstrings[0]["description"])
        self.assertIn("name", docstrings[0]["attributes"][0]["name"]) # Check nested structure

    def test_invalid_doctype(self):
        docstrings, code = self.few_shot_examples.examples("non_existent_type")
        self.assertEqual(len(docstrings), 0)
        self.assertEqual(len(code), 0)

    def test_empty_doctype(self):
        docstrings, code = self.few_shot_examples.examples("")
        self.assertEqual(len(docstrings), 0)
        self.assertEqual(len(code), 0)

    def test_statemachine_examples(self):
        docstrings, code = self.few_shot_examples.examples("statemachine")
        self.assertEqual(len(docstrings), 4)
        self.assertEqual(len(code), 4)
        self.assertIn("state Thinking", code[0])
        self.assertIn("State machine for a dining philosopher problem simulation", docstrings[0]["summary"])
        self.assertIn("pseudostates", docstrings[0]) # Check if the key exists
        self.assertIsInstance(docstrings[0]["pseudostates"], list) # Check type of nested element

if __name__ == '__main__':
    unittest.main()