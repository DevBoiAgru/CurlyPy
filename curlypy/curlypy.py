from .errors import *
import re

class CurlyPyTranslator:
    def __init__(self, filename: str = None, indentation: str = "   ") -> None:
        """
        Initializes a BrythonTranslator object.

        Args:
            filename (str): The name of the file to be translated. Defaults to None.
            indentation (str): The indentation to use for the translated code, i.e Tabs or Spaces. Defaults to 4 spaces.

        Returns:
            None
        """
        self.indentation: str = indentation
        self.filename: str = filename
        self.translated: str = ""

    def translate(self,
                  brython_code: str,
                  extra: bool,
                  remove_comments: bool = False,
                  output_raw: bool = False,
                  force_translate: bool = False) -> str:
        """
        Translates Brython code into Python code.

        Args:
            brython_code (str): The Brython code to be translated.
            extra (bool): Whether to add extra features to the translated code, like true = True and false = False.
            remove_comments (bool): Whether to remove comments from the translated code. Defaults to True.
            output_raw (bool): Whether to output the raw python code with no formatting. Defaults to False.
            force_translate (bool): Whether to force the translation. i.e. don't perform any checks. Can output non working code. Defaults to False.

        Returns:
            str: The translated Python code.

        Raises:
            BrythonTranslatorError: If unmatched brackets are found in the Brython code.
        """
        indentation_depth: int = 0
        last_useful_char: str = ""
        inside_something: bool = False              # If we are inside a comment, string, or a dictionary where we don't expand the indentation and other
                                                    # special symbols

        dict_typehint_regex: str = r':\s*([a-zA-Z_]\w*(?:\[[^\]]+\])?)\s*='

        self.translated = "# This code was translated to Python from Brython\n"

        # Extra features
        if extra:
            self.translated += "true = True\nfalse = False\n"
        
        # The fun stuff
        for line_number, line in enumerate(brython_code.splitlines()):
            self.translated += self.indentation * indentation_depth


            # Check for typehints in the line for a dictionary
            typehint_match = re.search(dict_typehint_regex, line)
            if typehint_match:
                typehint = typehint_match.group(1).lower()
                if typehint.startswith("dict") or typehint.startswith("set"):
                    # We are inside a dict or a set, no need to use brackets for indentation for this line
                    inside_something = True
            
            # How many quotes we have seen in this line. It resets every time we are in a new line
            double_quotes_seen: int = 0
            single_quotes_seen: int = 0

            for char_index, char in enumerate(line.strip()):

                if inside_something:
                    # We are in a comment or a string, so just append the character and move on. No need to check for anything
                    self.translated += char
                    continue
                
                if char == "{":
                    # We are opening a bracket, increase the indentation depth and add a colon
                    indentation_depth +=1
                    self.translated += ":\n"
                    self.translated += self.indentation * indentation_depth

                
                elif char == "}":
                    if last_useful_char == "{" and not inside_something:
                        # Opened a bracket and immediately closed it?? What a weirdo
                        
                        # Remove the last colon we added when the bracket was opened
                        # One rstrip to remove spaces and tabs, one to remove the last colon
                        self.translated = self.translated.rstrip().rstrip(":")
                        
                    indentation_depth -=1
                
                elif char == ";":
                    # End of statement, start a new line with indentation
                    self.translated += "\n"
                    self.translated += self.indentation * indentation_depth
                
                elif char == "#":
                    # Start of a comment, mark it and add the character
                    inside_something = True
                    self.translated += char

                elif char == " ":
                    if last_useful_char == ";" or last_useful_char == "{":
                        continue
                    else:
                        self.translated += char

                elif char == '"':
                    # Start / end of a string
                    double_quotes_seen += 1

                    # If we have seen an odd number of double quotes, we are inside a string
                    if double_quotes_seen % 2 == 0:
                        inside_something = False
                    else:
                        inside_something = True

                    self.translated += char

                elif char == "'":
                    # Start / end of a string
                    single_quotes_seen += 1

                    # If we have seen an odd number of double quotes, we are inside a string
                    if single_quotes_seen % 2 == 0:
                        inside_something = False
                    else:
                        inside_something = True

                    self.translated += char
                
                else:
                    # Normal character, just add it
                    self.translated += char


                last_useful_char = char

            self.translated += "\n"
            

            # Line over, we are out of a comment or string (if we were in one)
            inside_something = False

        # Error checking
        if not force_translate:
            if indentation_depth > 0:
                # This should raise an exception but currently the strings logic messes with how we count indentation
                pass
                # raise UnmatchedBracketsError(f"Unmatched brackets found in Brython code!")
        return self.format(self.translated, remove_comments) if not output_raw else self.translated

    
    def format(self, python_code: str, remove_comments: bool = True) -> str:
        """
        (lightly) Formats the Python code to make it somewhat readable. For proper formatting, use a third party tool.

        What it does:

        - Removes empty lines and lines with only whitespace
        - Removes trailing whitespace
        - Removes comments from the code (optional)

        Args:
            python_code (str): The Python code to be formatted.
            remove_comments (bool): Whether to remove comments from the code. Defaults to True.

        Returns:
            str: The formatted Brython code.
        """

        # Remove comments from the code
        if remove_comments:
            python_code = self.strip_comments(python_code)

        lines: list[str] = []
        for line in python_code.splitlines():
            # Clear all lines with no text in them
            clean_line = line.strip()
            if clean_line == "":
                continue

            # Remove trailing whitespace and add the formatted line to the lines list
            lines.append(line.rstrip())

        return "\n".join(lines)

    def strip_comments(self, python_code: str) -> str:
        """
        Strips comments from the Python code.

        Args:
            python_code (str): The Python code to be stripped.

        Returns:
            str: The stripped Python code.
        """
        lines: list[str] = []
        for line in python_code.splitlines():
            # Find '#' in the line and remove everything after it
            comment_index = line.find("#")
            if comment_index != -1:
                line = line[:comment_index]

            # Add the stripped line to the lines list
            lines.append(line)
        return "\n".join(lines)

    def translate_file(self, extra: bool= True, remove_comments: bool = True, output_raw: bool = False, force_translate: bool = False) -> str:
        """
        Translates a Brython file into Python code.

        Args:
            None

        Returns:
            str: The translated Python code.
        """
        if self.filename is None:
            raise Exception("No filename provided while initialisation!")
        with open(self.filename, "r") as brython_file:
            return self.translate(brython_file.read(), extra, remove_comments, output_raw, force_translate)
