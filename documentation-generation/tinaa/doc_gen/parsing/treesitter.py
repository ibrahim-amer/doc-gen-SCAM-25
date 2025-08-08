from tinaa.doc_gen.call_model import CallModel
from tinaa.doc_gen.helpers import Helpers
from tinaa.doc_gen.config.BaseLLM import BaseLLM
from tree_sitter import Parser
from tree_sitter_language_pack import get_language #, get_parser


class ParseFile:
    """
    Class for parsing code files and adding docstrings based on language specifications.
    """
    def __init__(self, llm_model: BaseLLM):
        self.llm_model = llm_model
    # Helper function to determine indentation
    def get_indentation_level(self, code : str, start_byte: int) -> int:
        """
        Calculates the indentation level of the current line in the given code string.
        
        Parameters
        ----------
        code
            The code string to analyze for indentation.
        start_byte
            The byte index to determine the current line indentation.
        
        Returns
        -------
        :
            The number of spaces or tabs at the start of the current line.
        
        """
        
        line_start = code.rfind('\n', 0, start_byte) + 1  # Find the start of the current line
        indentation = 0
        while line_start + indentation < len(code) and code[line_start + indentation] in " \t":
            indentation += 1
        return indentation
    
    # Function to check if there's an existing docstring or comment
    def has_docstring_or_comment(self,node, doc_type: str) -> bool:
        """
        Checks if a node has a docstring or comment based on the specified documentation type.
        
        Parameters
        ----------
        node
            The node to check for a docstring or comment.
        doc_type
            The type of documentation to check for (e.g., numpydoc, tsdoc).
        
        Returns
        -------
        :
            Returns True if a docstring or comment is found, otherwise False.
        
        """
        
        if doc_type == 'numpydoc':  # Python docstring check
            # For Python, check if the first statement in the function body is a string (docstring)
            body_node = node.child_by_field_name('body')
            if body_node and body_node.child_count > 0:
                first_statement = body_node.child(0)
                # Check if the first statement is a string, which would be a docstring
                return first_statement.type == 'expression_statement' and first_statement.child(0).type == 'string'
        elif doc_type == 'tsdoc':
            if node.type == 'export' or node.type == 'decorator':
                parent_sibling = node.parent.prev_sibling
                previous_sibling = node.prev_sibling
                if previous_sibling and previous_sibling.type:
                    if previous_sibling.type == 'comment' or previous_sibling.type == 'block_comment':
                        return True
                if parent_sibling and parent_sibling.type:
                    if parent_sibling.type == 'comment' or parent_sibling.type == 'block_comment':
                        return True
            else:
                previous_sibling = node.prev_sibling
            # print(previous_sibling.type, 'previous')
            if previous_sibling and previous_sibling.type:
                # print(previous_sibling.type, 'type')
                return previous_sibling.type == 'comment' or previous_sibling.type == 'block_comment'
        else:  
            # For Java/TypeScript, check if the previous sibling is a comment 
            previous_sibling = node.prev_sibling
            # print(previous_sibling, 'prev')
            # print(previous_sibling.type, 'previous')
            if previous_sibling and previous_sibling.type:
                return previous_sibling.type == 'comment' or previous_sibling.type == 'block_comment'
        return False
    

    def check_file(self, code : str, unicorn: bool, language_info : dict, debug=True) -> str:
        """
        Generates documentation for the provided code based on language-specific elements.
        
        Parameters
        ----------
        code
            The source code to be documented as a string.
        unicorn
            A string parameter used for documentation generation.
        language_info
            A dictionary containing language-specific information.
        debug
            A boolean flag to enable or disable debugging output.
        
        Returns
        -------
        :
            The modified code with inserted documentation as a string.
        
        """
        
        elements_to_document = language_info['elements_to_document']
        # print(elements_to_document)
        doc_type = language_info['doc_format']
        # print(language_info)
        language = language_info['language']
        LANGUAGE_PARSER = get_language(language.lower())

        # Set the language for the parser
        parser = Parser(LANGUAGE_PARSER)
        tree = parser.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        # print(root_node)
        modified_code = code  # Start with the original code
        insertions = []  # To store the positions to insert the docstrings

        def add_docstring(node)-> None:
            """
            Adds a docstring to a class or function declaration if none exists.
            
            Parameters
            ----------
            node
                The node representing a class or function declaration in the parse tree.
            
            """
            
            # Check if the node is a class or method/function declaration
            if node.type in elements_to_document:
                elementInfo = {} #use if we want to find extra info from the parse tree to pass in prompt
                #elementInfo = self.get_element_info(node)
                identifier_node = node.child_by_field_name("name")
                if identifier_node:
                    current_func_name = identifier_node.text.decode("utf8")
                    print(f"Found {node.type}: {current_func_name}")
                else:
                    current_func_name = node.type
                # Mark where to insert the docstring
                start_of_function = node
                if language.lower() == 'typescript' and node.prev_sibling and node.prev_sibling.type == 'export':
                    start_of_function = node.prev_sibling                
                if start_of_function and start_of_function.prev_sibling and start_of_function.prev_sibling.type == 'decorator':
                    start_of_function = start_of_function.prev_sibling

                start_byte = start_of_function.start_byte
                end_byte = node.end_byte
                if not self.has_docstring_or_comment(start_of_function, doc_type):
                    code_segment = modified_code[start_byte:end_byte]
                    # Calculate the indentation level
                    indent_level = self.get_indentation_level(modified_code, start_byte)
                    code_type = node.type.lower()
                    docstring = CallModel(self.llm_model).insert_docstring(current_func_name, code_segment, code_type, doc_type.lower(), unicorn, language, elementInfo)
                    
                    if docstring: #dont insert empty string when theres an error
                        if doc_type == "numpydoc":
                            end_decl = node.child_by_field_name('body'),start_byte
                            for child in node.children:
                                if child.type == ':':
                                    end_decl = child.end_byte
                            insertion_point = end_decl
                            indented = Helpers().indent_docstring(docstring, indent_level)
                            if indented and indented[-1] == "":
                                indented.pop()
                            indented_docstring = '\n'.join(indented)
                            insertions.append((insertion_point, f"\n{indented_docstring}"))
                        else:
                            indented = Helpers().indent_docstring(docstring, indent_level - 4)
                            if indented and indented[-1] == "":
                                indented.pop()
                            indented_docstring = '\n'.join(indented)
                            indent_string = ' ' * indent_level
                            insertions.append((start_byte,  '\n' + f"{indented_docstring}" + '\n' + indent_string))
                else:
                    print(f"Docstring or comment already exists for {current_func_name}, skipping.")
            # For inner functions/classes
            for child in node.children:
                add_docstring(child)


        # Start traversing from the root node
        add_docstring(root_node)

        # Apply the insertions to the original code
        for position, string_to_insert in sorted(insertions, key=lambda x: x[0], reverse=True):
            modified_code = modified_code[:position] + string_to_insert + modified_code[position:]

        #Add help rules foe Makefiles to display the documentation from Makehelp format
        # if doc_type == "makedoc":
        #     modified_code = Helpers().add_makehelp_rules(modified_code)

        return modified_code
