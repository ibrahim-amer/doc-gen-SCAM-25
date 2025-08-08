from tinaa.doc_gen.call_model import CallModel
from tinaa.doc_gen.helpers import Helpers
from arpeggio import *
from arpeggio import RegExMatch as _


#UNUSED
def t_innerblock():     return symbol, ZeroOrMore(string_literal), '{', ZeroOrMore(t_instruction), '}'
def string():           return [ _(r'"\$\{.*?\}"'), _(r'"\{.*?\}"'), _(r'".*?"'), _(r"'.*?'")]

#COMMENT FORMATS
def pythoncomment():    return [_(r"#.*"), _(r'(?s)"""(.*?)"""'), _(r"(?s)'''(.*?)'''")]
def javacomment():      return [_(r"//.*"), _(r"(?s)/\*.*?\*/")]
def artcomment():      return [_(r"(?s)/\*.*?\*/")]

#COMMON GRAMMARS
#Lines ending with ; except };
# def instruction():    return [_(r'.*\{\}.*;$'), _(r'[^{}};]*;$'), _(r'.*\"\}\".*;$'), _(r'.*\"\{\".*;$'), _(r'.*; *//.*$'), ('return', _(r'[^;]*?;'))]
def closingBracket():   return '}', Optional(';')
def uppercaseWord():    return _(r"[A-Z][A-Za-z0-9_]*")


#ART
def art():                    return ZeroOrMore([art_capsule, art_protocol, art_class, statemachine])
def art_protocol():           return Kwd("protocol"), symbol, art_protocol_block
def art_protocol_block():     return '{', ZeroOrMore([art_declarations, embedded_code, art_in_event, art_out_event]), closingBracket
def art_in_event():           return Kwd('in'), event_code
def art_out_event():          return Kwd('out'), event_code
def event_code():             return symbol, '(', Optional(embedded_code), ')', Optional(';')
def art_class():            return Kwd("class"), symbol, Optional(':', [embedded_code, uppercaseWord]) ,capsule_block

def art_capsule():            return Kwd("capsule"), symbol, Optional(':', [embedded_code, uppercaseWord]) ,capsule_block
def capsule_block():          return '{', ZeroOrMore([art_declarations, statemachine, port, part, connect, embedded_code]), closingBracket

def port():                   return ZeroOrMore(['service', 'notify', 'behavior']), Kwd("port"), portItem, ZeroOrMore(',', portItem), Optional(';')
def portItem():               return symbol, Optional('~'), ':', uppercaseWord
def part():                 return Optional('optional'), Optional('plugin'), Kwd('part'), partItem, ZeroOrMore(',', partItem), Optional(';')
def partItem():             return symbol, Optional('~'), Optional(art_declarations), ':', uppercaseWord, Optional('[0..1]')
def connect():              return Kwd('connect'), chained_symbol, 'with', chained_symbol , Optional(';')
def redefine():            return Kwd('redefine'), transition
def chained_symbol():       return symbol, ZeroOrMore('.', symbol), ZeroOrMore(",", symbol, ZeroOrMore('.', symbol))
def statemachine():           return Kwd("statemachine"), art_state_machine_block
def art_state_machine_block(): return '{', ZeroOrMore([state, pseudoState, transition, redefine, embedded_code]), closingBracket
def transition():              return chained_symbol, Optional(":", [(art_declarations, symbol),chained_symbol]), '->', [art_on,(chained_symbol, art_on), when, chained_symbol,symbol], Optional(';')
def pseudoState():             return [Kwd('choice'), Kwd('junction'), Kwd('exitpoint'), Kwd('entrypoint')], symbol, ZeroOrMore(",", symbol),Optional(';')
def when():                  return symbol, Kwd('when'), Optional(embedded_code)
def state():                 return Kwd("state"), Optional("redefine"),uppercaseWord, Optional(art_declarations), Optional(state_block), ZeroOrMore(',', (uppercaseWord, Optional(art_declarations),Optional(state_block))), Optional(';')
def state_block():            return '{', ZeroOrMore([state, pseudoState, art_on, transition, (Optional(['entry', 'exit']), embedded_code)]), closingBracket
def art_on():                 return Optional([(chained_symbol, ':'), (chained_symbol, '->', chained_symbol, ':')]), Kwd("on"), chained_symbol, Optional("()"), Optional(embedded_code), Optional(';')
def art_declarations():       return '[[', Kwd("rt"), '::', symbol, Optional('(', t_instruction,')'), ']]' 
def code_pattern():           return [_(r"[^`]+")]
def embedded_code():          return '`', Optional(code_pattern), '`', Optional(';')


#TERRAFORM
def terraform():              return ZeroOrMore(t_statements)

#Terraform String
def connectors():             return ['.', '/', '-', '@']
def t_assignment():           return symbol, '=', [string_literal, t_funccall,t_variable]
# def t_path():                 return Optional(symbol), ZeroOrMore('/', [symbol, interpolation])
# def operator():               return ZeroOrMore([operator, interpolation, t_variable]), ['|'], ZeroOrMore([operator, interpolation, t_variable])
def t_expression():           return [conditional_expression, t_assignment, t_funccall, string_literal, t_variable]
def conditional_expression(): return comparison, '?', t_expression, ':', t_expression
def comparison():             return symbol, '==', [string_literal, literal, t_variable]
def t_funccall():             return symbol, '(', Optional(t_expression), ZeroOrMore(',',t_expression), ')'
def symbol():                 return _(r"\w+")
def literal():                return _(r'\d*\.\d*|\d+|".*?"|\w+(\[\w+\])?')

# Block types
def type():                  return [Kwd("provisioner"), Kwd("sku"), Kwd("resource"), Kwd('email_receiver'), Kwd("connection"), Kwd("data"), Kwd("site_config"), Kwd("variable"), Kwd("lifecycle"), Kwd("identity"), Kwd("logs"), Kwd("output"), Kwd("module"),  Kwd("root_block_device"), Kwd("backend"), Kwd("locals"), Kwd("terraform"), Kwd("provider"), Kwd("output"), Kwd("required_providers"), Kwd("required_version"), Kwd("dynamic"), Kwd("count"), Kwd("for_each"), Kwd("depends_on"), Kwd("ingress"), Kwd("outgress")]
def decl():                  return [type, symbol], ZeroOrMore(string_literal)
def block():                 return decl, "{", ZeroOrMore(t_statements), "}"

#Inside Block
def t_statements():           return [block, t_dict, t_instruction]
def t_instruction():          return symbol, "=", [string_literal, t_array, t_variable, eof, xml, query]
def t_dict():                 return symbol, '=', '{', ZeroOrMore(t_instruction), '}'

#Variables
def t_array():                return '[', [(items, ZeroOrMore(',', items), Optional(',')), eof, xml, query], ']'         
def t_variable():             return Optional([t_funccall, interpolation, symbol]), Optional(t_array), ZeroOrMore(connectors, [t_funccall, interpolation, symbol], Optional(t_array))
def string_literal():         return [('"', ZeroOrMore([interpolation, t_variable, '|']), '"'), string]
def interpolation():          return '${', t_expression, '}', Optional(symbol)
def eof():                    return   _(r'<<EOF[\s\S]*?EOF')
def items():                  return [string_literal, t_variable]
def xml():                    return _(r'<<XML[\s\S]*?XML')
def query():                    return _(r'<<-QUERY[\s\S]*?QUERY')

positions = []

#MUST ADD VISITOR CLASSES FOR SCRIPT TO WORK
class Visitor(PTNodeVisitor):
    #TERRAFORM
    def visit_block(self, node, children):
        start_pos = node.position
        end_pos = node.position_end
        positions.append((start_pos, end_pos, node.rule_name, 'block'))

        print(f"{node.rule_name} found from position {start_pos} to {end_pos}")
        return start_pos
    #ART
    def visit_statemachine(self, node, children):
        start_pos = node.position
        end_pos = node.position_end
        positions.append((start_pos, end_pos, node.rule_name, 'block'))

        print(f"{node.rule_name} found from position {start_pos} to {end_pos}")
        return start_pos
    # def visit_art_class(self, node, children):
    #     start_pos = node.position
    #     end_pos = node.position_end
    #     positions.append((start_pos, end_pos, node.rule_name, 'block'))

    #     print(f"{node.rule_name} found from position {start_pos} to {end_pos}")
    #     return start_pos
    def visit_art_capsule(self, node, children):
        start_pos = node.position
        end_pos = node.position_end
        positions.append((start_pos, end_pos, node.rule_name, 'block'))

        print(f"{node.rule_name} found from position {start_pos} to {end_pos}")
        return start_pos

# def main(debug=False):

#     test = """
#     `
#         private: int count = 0;
#     `
#    """

#     parser = ParserPython(embedded_code, pythoncomment, debug=debug)
#     parse_tree = parser.parse(test)
#     name = visit_parse_tree(parse_tree, Visitor(debug=debug))
#     print(name)
# if __name__ == "__main__":
#     main(debug=True)

class Arpeg:

    def __init__(self):
        """
        Initializes a new instance of the class.
        
        Parameters
        ----------
        self : object
            The instance of the class.
        
        Returns
        -------
        None
        """
        self.currentType = ""
        self.type = None
        self.full_declaration = []
        self.current_block = []

    def has_docstring(self, doc_format: str, lines: list, i: int)-> bool:
        """
        Check if a code chunk contains a docstring in the specified language.
        
        Parameters
        ----------
        language : str
            The programming language of the code chunk. Can be 'python' or 'java'.
        lines : list
            The lines of code in the code chunk.
        i : int
            The index of the current line being processed.
        
        Returns
        -------
        bool
            True if a docstring is found, False otherwise.
        
        Raises
        ------
        None
        """
        match = False
        if doc_format == 'artdoc':
            j = i - 2            
            while j >= 0:
                stripped_line = lines[j].strip()
                if stripped_line == "*/":  # End of Javadoc comment
                    match = True
                elif not stripped_line.startswith("*") and stripped_line:
                    # If we encounter a non-comment, non-empty line, stop checking
                    break
                j -= 1
        elif doc_format == 'hashcomment':
            j = i - 2 
            while j >= 0:
                stripped_line = lines[j].strip()
                if stripped_line.startswith('#'):  # Start of hash comment
                    match = True
                elif stripped_line:
                    break
                j -= 1
        return match

    # Helper function to determine indentation
    def get_indentation_level(self, code: str, start_byte: int)-> int:
        """Returns the indentation level (in spaces) based on the start of the line."""
        line_start = code.rfind('\n', 0, start_byte) + 1  # Find the start of the current line
        indentation = 0
        while line_start + indentation < len(code) and code[line_start + indentation] in " \t":
            indentation += 1
        return indentation  
      
    def check_file(self, code: str, unicorn: bool, language_info: dict, debug=True) -> str:
        """
        Check the file for declarations and update the code with docstrings.
        
        Parameters
        ----------
        code : str
            The code to be checked and updated.
        file_name : str
            The name of the file being checked.
        unicorn : bool
            A boolean indicating whether the code uses unicorn.
        language : str
            The programming language of the code.
        
        Returns
        -------
        str
            The updated code with added docstrings.
        """
        modified_code = code  # Start with the original code
        insertions = []
        self.helpers = Helpers()
        lines = code.split('\n')
        decl_start_index = 0
        language = language_info['language']
        doc_type = language_info['doc_format']

        #Default Terraform
        parser = ParserPython(terraform, pythoncomment, debug=debug)
        if language == 'art':
            parser = ParserPython(art, javacomment, debug=debug)
        parse_tree = parser.parse(code)
        name = visit_parse_tree(parse_tree, Visitor(debug=debug))
        for position in positions:
            start = position[0]
            end = position[1]
            rule_name = position[2]
            decl_start_index, col = parser.pos_to_linecol(start)
            code_block = code[start: end]

            if (not self.has_docstring(doc_type, lines, decl_start_index)) and code_block:
    
                indent_level = self.get_indentation_level(modified_code, start)

                docstring = CallModel().insert_docstring(rule_name.lower(), code_block, rule_name.lower(), doc_type.lower(), unicorn, language)
                if docstring: 
                    indented_docstring = '\n'.join(Helpers().indent_docstring(docstring, indent_level - 4))
                    indent_string = ' ' * indent_level
                    insertions.append((start,  '\n' + f"{indented_docstring}" + '\n' + indent_string))
                # Apply the insertions to the original code
        
        for position, string_to_insert in sorted(insertions, key=lambda x: x[0], reverse=True):
            modified_code = modified_code[:position] + string_to_insert + modified_code[position:]

        # Return the whole modified file as a string
        return modified_code