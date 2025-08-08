import openai, yaml, os, re, ast, time
from collections import defaultdict
from yaml import CLoader
from tinaa.doc_gen.helpers import Helpers
from tinaa.doc_gen.few_shot_examples import FewShotExamples
from tinaa.doc_gen.config.BaseLLM import BaseLLM
import google.generativeai as genai
import importlib.resources as resources

class CallModel:
    """
    Class for interacting with language models to generate completions and docstrings.
    """
    def __init__(self, llm_model: BaseLLM):
        """
        Initialize CallModel with a specific LLM backend.

        Parameters
        ----------
        llm : BaseLLM
            A concrete implementation of the BaseLLM interface 
            (e.g., OpenAILLM, GeminiLLM, TelusLLM).
        """
        self.llm_model = llm_model
    def call_model(self, messages: list[dict], temperature: float = 0.3) -> str:
        """
        Delegates the prompt to the injected LLM and returns the completion.

        Parameters
        ----------
        messages : list of dict
            A list of messages (chat format) to send to the model.
        temperature : float
            Controls randomness in generation (default: 0.3).

        Returns
        -------
        str
            The generated output from the language model.
        """
        return self.llm_model.generate(messages)
    
    def insert_docstring(self, name: str, code: str, codeType: str, docType: str, unicorn: bool, language: str, elementInfo = None):
        """
        Generate a docstring for a given code snippet based on its parameters and language.
        
        Parameters
        ----------
        name : str
            The name of the function or code block for which the docstring is being generated.
        code : list
            A list of strings representing the lines of code to be documented.
        codeType : str
            The type of code (e.g., function, class) being documented.
        file_name : str
            The name of the file containing the code.
        unicorn : bool
            A flag indicating whether to use a specific feature or tool (e.g., a documentation generator).
        language : str
            The programming language of the code (e.g., 'python').
        
        Returns
        -------
        str
            The generated docstring for the provided code snippet.
        
        Raises
        ------
        Exception
            If an error occurs during the docstring generation process, including issues with the input parameters or the documentation generation tools.
        """
        docstring = """"""
        try:
            print("GENERATING documentation for:" + name)
            docstring = self.generate_docstring(code, codeType, docType, unicorn, language, elementInfo)
            print('Docs Generated.')

        except Exception as e:
            print(e)
            code = code[:8000]
            print(name, ': error occured while generating docstring, trying again in 10 seconds')
            time.sleep(10)
            docstring = self.generate_docstring(code, codeType, docType, unicorn, language, elementInfo)

        return docstring
    

    def generate_docstring(self, code: str, code_type: str, doc_type: str, unicorn: bool, language: str, elementInfo = None):
        """
        Generates a docstring for the provided code using a specified model and templates.
        
        Parameters
        ----------
        code
            The code snippet for which to generate a docstring.
        code_type
            The type of code (e.g., function, class) to be documented.
        doc_type
            The doc format to use.
        unicorn
            The model or API used for generating documentation.
        language
            The programming language of the provided code.
        elementInfo
            Optional additional information about the code elements.
        
        Returns
        -------
        :
            A string containing the generated docstring or an empty string if generation fails.
        
        """
        self.helpers = Helpers()
        #To be rendered into Jinja prompt template
        data = {
            'language' : language,
            'doc_type' : doc_type,
            'code_type': code_type
        }
        messages = [ {"role": "system", "content": 
        "You are an expert {} programmer tasked with providing a dictionary with values describing a comment to the provided code.".format(language)} ]
        
        #Few shot examples
        docstrings, example_code = FewShotExamples().examples(code_type)
        for i in range(len(docstrings)):
            messages.append(
                {"role": "user", "content": 'Please comment the provided ' + code_type + ': ' + str(example_code[i])}
            )   
            messages.append(
                {"role": "assistant", "content": str(docstrings[i])},
            )   

        dict_skeleton = self.extract_dict_keys(data, elementInfo) #Build dictionary skeleton
        data['template'] = dict_skeleton
        data['code'] = code

        template_package = "tinaa.doc_gen.jinja_templates"

        # Get the real path of the template inside the package
        template_path = resources.files(template_package).joinpath("prompt_template.j2")

        prompt_template = str(template_path)

        prompt = self.helpers.read_jinja_template(prompt_template, data) #render into Jinja prompt template

        messages.append(
                {"role": "user", "content": prompt},
        )
        filled_dict = self.call_model(messages, 0.3) #LLM call
        filled_dict = self.extract_dict(filled_dict, language, doc_type) #Extract dict from outputed string
        filled_dict = self.postprocess_dict(filled_dict) #Remove unwanted entries in dict
        if len(filled_dict):
            filled_dict.update(data) #prepare data to render into template
            docstring = self.render_docs(filled_dict) #render into doc_format template
            return docstring
        else:
            return ""

    def postprocess_dict(self, d: dict) -> dict:
        """
        Recursively processes a dictionary to remove unwanted string values.
        
        Parameters
        ----------
        d
            The input dictionary to be processed and filtered.
        
        Returns
        -------
        :
            A new dictionary with unwanted strings filtered out.
        
        """
        if isinstance(d, dict):
            return {
                k: self.postprocess_dict(v) for k, v in d.items()
                if not (isinstance(v, str) and v.lower().startswith(('none', 'n/a', 'void')))  # Check for unwanted strings
            }
        return d

    def render_docs(self, generated_dict: dict) -> str:
        """
        Converts a dictionary to a string using a Jinja template from a specified directory.
        
        Parameters
        ----------
        generated_dict
            A dictionary containing data to populate the Jinja template.
        
        Returns
        -------
        :
            The rendered string from the Jinja template, or an empty string if not found.
        
        """


        # Use importlib.resources to access the package directory safely
        template_package = "tinaa.doc_gen.jinja_templates.language_doc_templates"

        try:
            template_dir = resources.files(template_package)
        except (FileNotFoundError, ModuleNotFoundError):
            return """"""  

        for path in template_dir.iterdir():
            if path.is_file():
                rendered = Helpers().read_jinja_template(str(path), generated_dict)
                if rendered:
                    return rendered

        return """"""  
    
    def extract_dict(self, llm_output, language: str, doc_type: str) -> dict:
        """
        Extracts a dictionary from a formatted string within a docstring.
        
        Parameters
        ----------
        llm_output
            The input string containing a potential dictionary.
        language
            The programming language associated with the dictionary.
        doc_type
            The type of documentation for the dictionary.
        
        Returns
        -------
        :
            Returns the extracted dictionary or an empty dictionary on failure.
        
        Raises
        ------
        SyntaxError
            Raised if the docstring has invalid syntax.
        ValueError
            Raised if the docstring cannot be evaluated.
        
        """
        
        braces = 0
        start = None
        for i, c in enumerate(llm_output):
            if c == '{':
                if not braces: start = i
                braces += 1
            elif c == '}':
                braces -= 1
                if not braces:
                    llm_output = llm_output[start:i+1]
        if isinstance(llm_output, str):
            try:
                # Attempt to evaluate the string as a Python object
                dictionary = ast.literal_eval(llm_output)
                if isinstance(dictionary, dict):  # Ensure it's a dictionary
                    dictionary['language'] = language
                    dictionary['doc_type'] = doc_type
                    return dictionary
                else:
                    print("The evaluated structure is not a dictionary.")
                    return {}
            except (SyntaxError, ValueError):
                print("Invalid format, unable to parse the dictionary.")
                return {}

        else:
            print("Input is not a string.")
            return {}

    def extract_dict_keys(self, data: dict, elementInfo = None) -> str:
        """
        Extracts keys from Jinja templates based on provided data and element information.
        
        Parameters
        ----------
        data
            Data used to render the Jinja template.
        elementInfo
            Optional information about elements for processing.
        
        Returns
        -------
        :
            A string representation of a dictionary containing extracted keys and their values.
        
        """
        template_package = "tinaa.doc_gen.jinja_templates.language_doc_templates"

        try:
            template_dir = resources.files(template_package)
        except (FileNotFoundError, ModuleNotFoundError):
            return ''

        for template_path in template_dir.iterdir():
            if template_path.is_file():
                # Render the template with the current data
                rendered = Helpers().read_jinja_template(str(template_path), data)

                if rendered:
                    # Read the template content as text
                    with template_path.open('r', encoding='utf-8') as file:
                        template_content = file.read()

                    # Extract Jinja variables
                    keys = re.findall(r'{{\s*(.*?)\s*}}', template_content)

                    # Extract Jinja for-loops
                    for_loops = re.findall(r'\{\%\s*for\s+(\w+)\s+in\s+(\w+)\s*\-?\%\}', template_content)

                    result = {}
                    loop_history = {}
                    inner_dict = defaultdict(dict)

                    for loop_variable, iterable in for_loops:
                        result[iterable] = []
                        loop_history[loop_variable] = iterable

                    for key in keys:
                        parts = key.split('.')
                        if len(parts) == 1:
                            parent_key = parts[0]
                            result[parent_key] = '<placeholder>'
                        else:
                            parent_key, child_key = parts[0], parts[1]
                            if parent_key in loop_history:
                                loop_iterable = loop_history[parent_key]
                                inner_dict[parent_key][child_key] = '<placeholder>'
                                result[loop_iterable].append(inner_dict[parent_key])
                            else:
                                if parent_key not in result:
                                    result[parent_key] = {}
                                result[parent_key][child_key] = '<placeholder>'

                    # Convert result dict to string and add context
                    string_dict = str(dict(result))
                    string_dict = string_dict.replace("'parameters': [", "'parameters': [  # List of parameters (can be 0, 1 or multiple) ")
                    string_dict = string_dict.replace("'raises': [", "'raises': [  # List of raised exceptions (can be 0, 1 or multiple) ")
                    return string_dict

        return ''