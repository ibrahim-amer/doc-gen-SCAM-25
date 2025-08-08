import unittest
from unittest.mock import patch, MagicMock
from tinaa.doc_gen.call_model import CallModel

class TestCallModel(unittest.TestCase):
    def setUp(self):
        self.cm = CallModel()

    @patch("tinaa.doc_gen.call_model.client.chat.completions.create")
    def test_call_model_unicorn_telus_model(self, mock_telus_create):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Telus response"))]
        mock_telus_create.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        result = self.cm.call_model(unicorn=True, temp=0.5, messages=messages)
        self.assertEqual(result, "Telus response")
        mock_telus_create.assert_called_once()

    @patch("tinaa.doc_gen.call_model.genai.GenerativeModel")
    def test_call_model_gemini_model(self, mock_gemini_model):
        mock_chat = MagicMock()
        mock_chat.send_message.return_value.text = "Gemini response"
        mock_model_instance = MagicMock(start_chat=MagicMock(return_value=mock_chat))
        mock_gemini_model.return_value = mock_model_instance

        messages = "Hello Gemini"
        result = self.cm.call_model(unicorn=False, temp=0.1, messages=messages, pub_model='gemini')
        self.assertEqual(result, "Gemini response")
        mock_gemini_model.assert_called_once_with(
            'gemini-2.5-flash-preview-04-17',
            generation_config={'temperature': 0.1}
        )

    @patch("tinaa.doc_gen.call_model.openai.chat.completions.create")
    def test_call_model_openai_model(self, mock_openai_create):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="OpenAI response"))]
        mock_openai_create.return_value = mock_response

        messages = [{"role": "user", "content": "Hello OpenAI"}]
        result = self.cm.call_model(unicorn=False, temp=0.7, messages=messages)
        self.assertEqual(result, "OpenAI response")
        mock_openai_create.assert_called_once()

    @patch("tinaa.doc_gen.call_model.CallModel.render_docs")
    @patch("tinaa.doc_gen.call_model.CallModel.postprocess_dict")
    @patch("tinaa.doc_gen.call_model.CallModel.extract_dict")
    @patch("tinaa.doc_gen.call_model.CallModel.call_model")
    @patch("tinaa.doc_gen.call_model.CallModel.extract_dict_keys")
    @patch("tinaa.doc_gen.call_model.FewShotExamples")
    @patch("tinaa.doc_gen.call_model.Helpers")
    def test_generate_docstring_success(
        self, mock_helpers, mock_fewshot, mock_extract_dict_keys,
        mock_call_model, mock_extract_dict, mock_postprocess, mock_render_docs
    ):
        mock_helpers_instance = MagicMock()
        mock_helpers.return_value = mock_helpers_instance
        mock_helpers_instance.read_jinja_template.return_value = "Rendered prompt"

        mock_fewshot_instance = MagicMock()
        mock_fewshot.return_value = mock_fewshot_instance
        mock_fewshot_instance.examples.return_value = (
            ["docstring 1"], ["def foo(): pass"]
        )

        mock_extract_dict_keys.return_value = "{'key': 'value'}"
        mock_call_model.return_value = "{'key': 'value'}"
        mock_extract_dict.return_value = {"processed_key": "processed_value"}
        mock_postprocess.return_value = {"processed_key": "processed_value"}
        mock_render_docs.return_value = "Final rendered docstring"

        code = "def foo(): pass"
        docstring = self.cm.generate_docstring(
            code=code,
            code_type="function",
            doc_type="doc",
            unicorn=True,
            language="python"
        )

        self.assertEqual(docstring, "Final rendered docstring")
        mock_render_docs.assert_called_once()

    @patch("tinaa.doc_gen.call_model.CallModel.render_docs")
    @patch("tinaa.doc_gen.call_model.CallModel.postprocess_dict")
    @patch("tinaa.doc_gen.call_model.CallModel.extract_dict")
    @patch("tinaa.doc_gen.call_model.CallModel.call_model")
    @patch("tinaa.doc_gen.call_model.CallModel.extract_dict_keys")
    @patch("tinaa.doc_gen.call_model.FewShotExamples")
    @patch("tinaa.doc_gen.call_model.Helpers")
    def test_generate_docstring_returns_empty_on_empty_dict(
        self, mock_helpers, mock_fewshot, mock_extract_dict_keys,
        mock_call_model, mock_extract_dict, mock_postprocess, mock_render_docs
    ):
        mock_helpers_instance = MagicMock()
        mock_helpers.return_value = mock_helpers_instance
        mock_helpers_instance.read_jinja_template.return_value = "Rendered prompt"

        mock_fewshot_instance = MagicMock()
        mock_fewshot.return_value = mock_fewshot_instance
        mock_fewshot_instance.examples.return_value = (
            ["docstring 1"], ["def foo(): pass"]
        )

        mock_extract_dict_keys.return_value = "{'key': 'value'}"
        mock_call_model.return_value = "{'key': 'value'}"
        mock_extract_dict.return_value = {}
        mock_postprocess.return_value = {}
        mock_render_docs.return_value = "Should not be called"

        code = "def bar(): pass"
        docstring = self.cm.generate_docstring(
            code=code,
            code_type="function",
            doc_type="doc",
            unicorn=False,
            language="python"
        )

        self.assertEqual(docstring, "")
        mock_render_docs.assert_not_called()

    @patch("tinaa.doc_gen.call_model.CallModel.generate_docstring")
    def test_insert_docstring_success(self, mock_generate_docstring):
        mock_generate_docstring.return_value = "Generated docstring"
        result = self.cm.insert_docstring(
            name="my_func",
            code="def my_func(): pass",
            codeType="function",
            docType="doc",
            unicorn=False,
            language="python"
        )
        self.assertEqual(result, "Generated docstring")
        mock_generate_docstring.assert_called_once()

    @patch("tinaa.doc_gen.call_model.time.sleep", return_value=None)
    @patch("tinaa.doc_gen.call_model.CallModel.generate_docstring")
    def test_insert_docstring_retry_on_exception(self, mock_generate_docstring, mock_sleep):
        mock_generate_docstring.side_effect = [Exception("fail"), "Fallback docstring"]
        result = self.cm.insert_docstring(
            name="retry_func",
            code="def retry_func(): pass",
            codeType="function",
            docType="doc",
            unicorn=True,
            language="python"
        )
        self.assertEqual(result, "Fallback docstring")
        self.assertEqual(mock_generate_docstring.call_count, 2)
        mock_sleep.assert_called_once_with(10)

    @patch("tinaa.doc_gen.call_model.resources.files")
    @patch("tinaa.doc_gen.call_model.Helpers")
    def test_render_docs_successful(self, mock_helpers, mock_resources_files):
        mock_template_file = MagicMock()
        mock_template_file.is_file.return_value = True
        mock_template_file.open.return_value.__enter__.return_value.read.return_value = """
        **/
        value
        */
        """
        mock_resources_dir = MagicMock()
        mock_resources_dir.iterdir.return_value = [mock_template_file]
        mock_resources_files.return_value = mock_resources_dir

        mock_helpers.return_value.read_jinja_template.return_value = """
        **/
        value
        */
        """

        generated_dict = {"description": "value"}
        result = self.cm.render_docs(generated_dict)

        expected_result = """
        **/
        value
        */
        """
        self.assertEqual(result, expected_result)
        mock_helpers.return_value.read_jinja_template.assert_called_once()

    @patch("tinaa.doc_gen.call_model.resources.files")
    def test_render_docs_no_templates(self, mock_resources_files):
        mock_resources_dir = MagicMock()
        mock_resources_dir.iterdir.return_value = []
        mock_resources_files.return_value = mock_resources_dir

        result = self.cm.render_docs({"description": "value"})
        self.assertEqual(result, "")

    @patch("tinaa.doc_gen.call_model.Helpers")
    @patch("tinaa.doc_gen.call_model.resources.files")
    def test_render_docs_empty_renders(self, mock_resources_files, mock_helpers):
        mock_template_file = MagicMock()
        mock_template_file.is_file.return_value = True
        mock_template_file.open.return_value.__enter__.return_value.read.return_value = ""
        mock_resources_dir = MagicMock()
        mock_resources_dir.iterdir.return_value = [mock_template_file]
        mock_resources_files.return_value = mock_resources_dir

        mock_helpers.return_value.read_jinja_template.side_effect = ["", ""]

        result = self.cm.render_docs({"description": "value"})
        self.assertEqual(result, "")

    def test_postprocess_dict_removes_unwanted_strings(self):
        test_dict = {
            'key1': 'none value',
            'key2': 'valid string',
            'key3': {
                'subkey1': 'n/a data',
                'subkey2': 'useful data',
            }
        }
        expected = {
            'key2': 'valid string',
            'key3': {
                'subkey2': 'useful data',
            }
        }
        processed = self.cm.postprocess_dict(test_dict)
        self.assertEqual(processed, expected)

    def test_postprocess_dict_nested_removal(self):
        test_dict = {
            'a': 'None',
            'b': {
                'c': 'void result',
                'd': {
                    'e': 'n/a entry',
                    'f': 'keep me'
                }
            },
            'g': 'keep me too'
        }
        expected = {
            'b': {
                'd': {
                    'f': 'keep me'
                }
            },
            'g': 'keep me too'
        }
        result = self.cm.postprocess_dict(test_dict)
        self.assertEqual(result, expected)

    def test_postprocess_dict_empty_dict(self):
        result = self.cm.postprocess_dict({})
        self.assertEqual(result, {})

    def test_postprocess_dict_no_unwanted_strings(self):
        test_dict = {
            'x': 'hello',
            'y': 42,
            'z': {'a': 'world'}
        }
        result = self.cm.postprocess_dict(test_dict)
        self.assertEqual(result, test_dict)

    # def test_postprocess_dict_non_dict_input(self):
    #     input_data = ['none', 'n/a', 'void']
    #     result = self.cm.postprocess_dict(input_data)
    #     self.assertEqual(result, input_data)

    def test_extract_dict_valid_string(self):
        valid_dict_str = "{'key': 'value'}"
        result = self.cm.extract_dict(valid_dict_str, language='python', doc_type='doc')
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('key'), 'value')
        self.assertEqual(result.get('language'), 'python')
        self.assertEqual(result.get('doc_type'), 'doc')

    def test_extract_dict_invalid_string(self):
        invalid_dict_str = "not a dict"
        result = self.cm.extract_dict(invalid_dict_str, language='python', doc_type='doc')
        self.assertEqual(result, {})

    # def test_extract_dict_keys_returns_string(self):
    #     data = {'language': 'python', 'doc_type': 'numpydoc', 'code_type': 'function_declaration'}
    #     result = self.cm.extract_dict_keys(data)
    #     self.assertIsInstance(result, str)

    @patch("tinaa.doc_gen.call_model.resources.files")
    @patch("tinaa.doc_gen.call_model.Helpers")
    def test_extract_with_for_loop(self, mock_helpers, mock_resources_files):
        javadoc_template = """
        /**
        * {{ description }}
        * 
        * {% for param in parameters -%}
        * @param {{ param.name }} {{ param.description }}
        * {% endfor %}
        * @return {{ returns.description }}
        */
        """

        mock_template_file = MagicMock()
        mock_template_file.is_file.return_value = True
        mock_template_file.open.return_value.__enter__.return_value.read.return_value = javadoc_template

        mock_resources_dir = MagicMock()
        mock_resources_dir.iterdir.return_value = [mock_template_file]
        mock_resources_files.return_value = mock_resources_dir

        mock_helpers.return_value.read_jinja_template.return_value = "rendered output"

        result = self.cm.extract_dict_keys({})

        self.assertIn("{'description': '<placeholder>'", result)
        self.assertIn("{'parameters':", result)
