from jinja2 import Template

class Helpers:
    """
    A collection of helper functions for text processing and indentation handling.
    """

    #Help functions for make
    def add_makehelp_rules(self, code: str) -> str:
        """
        Adds help rules to a makefile if they are not already present.
        
        Parameters
        ----------
        code
            The makefile code to which help rules will be added.
        
        Returns
        -------
        :
            The updated makefile code with help rules added.
        
        """
        
        make_start = """
.PHONY: help

#@@ Generates a short help message for the makefile targets.
#@ This code uses awk to parse the makefile and generate a help message for the available targets. It prints the usage and a list of targets with their descriptions.
help:
	@awk 'BEGIN {FS = ":.*"; printf "\\nUsage:\\n  make \\033[36m<target>\\033[0m\\n"} /^[a-zA-Z_-]+:.*##/ { printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2 } /^#@@/ { prev_desc = substr($$0, 4) } /^[a-zA-Z_-]+:/ { if (prev_desc != "") { printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, prev_desc; prev_desc = "" } }' $(MAKEFILE_LIST)
            
#@@ Generates a long help message for the makefile targets.
#@ The code uses awk to parse the makefile and display help information for the specified target. It looks for lines starting with #@ to extract the description for the target. If the target is found, it prints the help information; otherwise, it displays a message indicating that no documentation was found for the specified target.
help-%:
	@awk -v rule=$* 'BEGIN {FS = ":.*"; found=0 } /^#@/ { prev_desc = substr($$0, 4) } \\
    /^[a-zA-Z_-]+:/ && $$1 == rule { \\
		if (prev_desc != "") { \\
			printf "\\nDocumentation for \\033[36m`%s`\\033[0m rule:\\n\\n", rule; \\
			printf "%s\\n", prev_desc; \\
			found=1; \\
			prev_desc = "" } }END { if (!found) printf "No documentation found for \\033[36m`make %s`\\033[0m\\n", rule }' $(MAKEFILE_LIST)                
            """
        if ".PHONY: help" not in code:
            code += ((f"\n{make_start}"))
        return code
    
    def make_file_find_comment_child(self, node, child_type) -> bool:
        """
        Checks if a node has a child of a specified type.
        
        Parameters
        ----------
        node
            The node object containing child elements to check.
        child_type
            The type of child to search for within the node.
        
        Returns
        -------
        :
            Returns True if a matching child type is found, otherwise False.
        
        """
        
        comment_child = False
        for child in node.children:
            if child.type == child_type:
                comment_child = True
        return comment_child

    def indent_docstring(self, docstring: str, indent_level: int) -> list:
        """
        Indents the given docstring with the specified indent level.
        
        Parameters
        ----------
        docstring:
            The docstring to be indented
        indent_level:
            The number of spaces to indent the docstring by
        
        Returns
        -------
            The indented docstring.
        """
        indentation_level = ' ' * (indent_level + 4)
        indented = []
        for line in docstring.split('\n'):
            indented.append(indentation_level + line)
        return indented
    
    def read_jinja_template(self, path: str, data: dict) -> str:
        """
        Read the Jinja template file and render it with the provided data.
        
        Parameters
        ----------
        path : str
            The file path of the Jinja template to be read.
        data : dict
            A dictionary containing the data to be used for rendering the template.
        
        Returns
        -------
        str
            The rendered template content as a string.
        
        Raises
        ------
        FileNotFoundError
            If the specified template file does not exist.
        """
        
        # Read the template file
        with open(path, 'r') as file:
            template_content = file.read()

            # Create the Jinja Template object
            template = Template(template_content)

            # Render the template with data
            return template.render(data)




#OLD HELPER FUNCTIONS
    # def reformat_docstring(self, docstring, max_line_length=100):
    #     """
    #     Reformats a Numpydoc-style docstring to ensure no line exceeds a specified length.

    #     Parameters
    #     ----------
    #     docstring : str
    #         The input Numpydoc docstring to reformat.
    #     max_line_length : int, optional
    #         The maximum allowed line length (default is 50 characters).
        
    #     Returns
    #     -------
    #     str
    #         The reformatted docstring with lines wrapped.
    #     """
    #     def wrap_line(line, max_len):
    #         """
    #         Wraps a string into lines of specified maximum length.
            
    #         Parameters
    #         ----------
    #         line
    #             The input string to be wrapped into lines.
    #         max_len
    #             The maximum length of each wrapped line.
            
    #         Returns
    #         -------
    #         :
    #             A list of strings, each representing a wrapped line.
            
    #         """
            
    #         words = line.split()
    #         wrapped_lines = []
    #         current_line = []
            
    #         for word in words:
    #             if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_len:
    #                 current_line.append(word)
    #             else:
    #                 wrapped_lines.append(" ".join(current_line))
    #                 current_line = [word]
            
    #         if current_line:
    #             wrapped_lines.append(" ".join(current_line))
            
    #         return wrapped_lines

    #     reformatted_lines = []
        
    #     for line in docstring.splitlines():
    #         # If the line exceeds the max length, break it
    #         if len(line) > max_line_length:
    #             reformatted_lines.extend(wrap_line(line, max_line_length))
    #         else:
    #             reformatted_lines.append(line)
        
    #     return "\n".join(reformatted_lines)

    # def get_indentation_level(self, line, multiline_start_index):
    #     """
    #     Calculate the indentation level of a given line.
        
    #     Parameters
    #     ----------
    #     line: str
    #         The line to calculate the indentation level for.
        
    #     Returns
    #     -------
    #     int:
    #         The calculated indentation level
    #     """
    #     if multiline_start_index:
    #         line = multiline_start_index
    #     leading_spaces = len(line) - len(line.lstrip())
    #     leading_tabs = line.count('\t')
    #     indentation = leading_spaces + leading_tabs * 4
    #     return indentation