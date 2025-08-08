from tinaa.doc_gen.parsing.arpeg import Arpeg
from tinaa.doc_gen.parsing.treesitter import ParseFile
import os, sys, json, yaml
from yaml import CLoader
from tinaa.doc_gen.config.config import Config
from tinaa.doc_gen.config.LLMFactory import LLMFactory

config = Config.load_from_file()
llm = LLMFactory.from_config(config, config.provider_enum)
print(llm)

file_path_origin = os.path.dirname(os.path.realpath(__file__))
# with open(f"{file_path_origin}/config/config.yaml", "r") as file:
#     config = yaml.load(file, Loader=CLoader)
class Main:
    def get_language_info(self, file_name: str):
        """
        Retrieve language information for a given file based on its extension.
        
        Parameters
        ----------
        
        file_name : str
            The name of the file for which language information is to be retrieved.
        
        Returns
        -------
        tuple 
            A tuple containing a dictionary of language information and a boolean indicating whether the language is to be documented.
        """
        lang_to_document = False
        # Path to JSON file
        file_path = f"{file_path_origin}/languages.json"
        info = {}
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            for lang in data['languages']:
                for ext in lang['extensions']:
                    if file_name.lower().endswith(ext.lower()):
                        info['parser'] = lang['parser'].lower()
                        info['doc_format'] = lang['doc_format'].lower()
                        info['language'] = lang['name'].lower()
                        info['extensions'] = lang['extensions']
                        if info['parser'] == 'treesitter':
                            info['elements_to_document'] = lang['elements_to_document']
                        lang_to_document = True

        return info, lang_to_document


    def process_file(self, file_path: str, file_name: str, unicorn: bool)-> None:
        """
        Process a file by removing existing docstrings and generating new ones.
        
        Parameters
        ----------
        file_path:
            The path of the file to be processed
        file_name:
            The name of the file
        unicorn:
            Choosing between public model and TELUS GenAI APIs
        """
        if file_path is None:
            print("No file path provided.")
            return

        language_info, lang_to_document = self.get_language_info(file_name)
        if (lang_to_document):
            with open(file_path, 'r') as f:
                print(file_name)
                if language_info['parser'] == 'arpeggio':
                    commented = Arpeg().check_file(f.read(), unicorn, language_info) #generate new docstrings

                else:
                    commented = ParseFile(llm_model=llm).check_file(f.read(), unicorn, language_info) #generate new docstrings

            with open(file_path, "w") as outfile:
                #write newly documented classes and functions to the file
                outfile.write(commented)
            # feedback = EvalDocs().eval_docs(commented, unicorn)
            # with open(file_path, "w") as outfile:
            #     #write newly documented classes and functions to the file
            #     outfile.write(commented)

    def parse_args(self,args):

        unicorn = True
        file_name = None
        thisdir = os.getcwd()


        args = [arg for arg in args if arg.strip()]
        if "-public" in args:
            unicorn = False
            args.remove("-public")

        if len(args) > 1:
            print("len args > 1")
            file_name = args[1]

        if (file_name):
            #documenting spcified file
            current_file_path = os.path.abspath(file_name)
            Main().process_file(current_file_path, file_name, unicorn)
        else:
            #walk through files in directory and generate docstrings for the classes and functions
            for r, d, f in os.walk(thisdir):
                for file in f:
                    if 'doc_gen' not in r and 'test' not in file and file != "__init__.py": #and file != "add_documentation.py" 
                        file_path = os.path.join(r, file)
                        Main().process_file(file_path, file, unicorn)
    
if __name__ == "__main__":
    Main().parse_args(sys.argv)


