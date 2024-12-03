from curlypy.errors import *
import re

class CurlyPyTranslator:
    def __init__(self, filename: str = None, indentation: str = "    ") -> None:
        """
        Initializes a CurlyPyTranslator object.

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
                  curlypy_code: str,
                  extra: bool = True,
                  remove_comments: bool = True,
                  output_raw: bool = False,
                  error_check: bool = True) -> str:
        """
        Translates CurlyPy code into Python code.

        Args:
            curlypy_code (str): The CurlyPy code to be translated.
            extra (bool): Whether to add extra features to the translated code, like true = True and false = False.
            remove_comments (bool): Whether to remove comments from the translated code. Defaults to True.
            output_raw (bool): Whether to output the raw python code with no formatting. Defaults to False.
            error_check (bool): Whether to perform basic syntax checks. Can output non working code if set to False. Defaults to True.

        Returns:
            str: The translated Python code.

        Raises:
            CurlyPySyntaxError: If syntax errors are found in the CurlyPy code.
        """
        indentation_depth: int = 0
        last_useful_char: str = ""


        self.translated: str = "# This code was translated to Python from CurlyPy\n"

        # Extra features
        if extra:
            self.translated += "true = True; false = False\n"
        
        # States
        in_double_quotes: bool = False
        in_single_quotes: bool = False
        in_comment      : bool = False
        in_collection   : bool = False          # Collection types like dict, set, list, tuple
                                                # Indentation isn't mandatory within these types

        typehint_regex: str = r":\s*([a-zA-Z0-9_]+)"
        collection_depth: int = 0

        # Data for errors
        bracket_stack: list[dict] = []          # Contains info about all the brackets opened and closed as a list of dicts

        # The fun stuff
        for line_number, line in enumerate(curlypy_code.splitlines()):
            self.translated += self.indentation * indentation_depth

            # Check for typehints in the line for a dictionary
            typehint_match = re.search(typehint_regex, line)
            
            if typehint_match:
                typehint = typehint_match.group(1).lower()
                if typehint in ["dict", "set", "list", "tuple"]:
                    # We are inside a collection, no need to use brackets for indentation for this line
                    in_collection = True

            for char_index, char in enumerate(line.strip()):

                if in_comment:
                    # We are in a comment, no need to check for anything
                    self.translated += char
                    continue
                
                if char == "{" and not (in_double_quotes or in_single_quotes):
                    if in_collection:
                        collection_depth +=1
                        self.translated += char
                    else:
                        # We are opening a bracket for indentation, increase the indentation depth and add a colon
                        indentation_depth +=1
                        self.translated += ":\n"
                        self.translated += self.indentation * indentation_depth

                
                elif char == "}":
                    if last_useful_char == "{" and not (in_comment or in_double_quotes or in_single_quotes):
                        # Opened a bracket and immediately closed it?? What a weirdo
                        
                        # Remove the last colon we added when the bracket was opened
                        # One rstrip to remove spaces and tabs, one to remove the last colon
                        # This is required since we added the colon and spaces when the bracket was opened
                        self.translated = self.translated.rstrip().rstrip(":")
                    
                    if (in_single_quotes or in_double_quotes):
                        # We are in a string, no need to change the indentation
                        self.translated += char
                        continue

                    # Check if a collection was closed or a code block was closed
                    if in_collection:
                        collection_depth -=1
                        self.translated += char
                        if collection_depth == 0:
                            in_collection = False
                    else:
                        # We are closing a bracket for indentation, decrease the indentation depth
                        indentation_depth -=1
                        self.translated += "\n"
                        self.translated += self.indentation * indentation_depth


                elif char == ";":
                    # Check if we are in a string. This check is required for all symbols
                    # which are replaced dynamically
                    if (in_single_quotes or in_double_quotes):
                        self.translated += char
                        continue
                    # End of statement, start a new line with indentation
                    self.translated += "\n"
                    self.translated += self.indentation * indentation_depth
                
                elif char == "#":
                    # Start of a comment, mark it and add the character
                    in_comment = True
                    self.translated += char

                elif char == " " and not (in_single_quotes or in_double_quotes):
                    # We do not care about spaces after these symbols
                    if last_useful_char in [";", "{", "}"]:
                        continue
                    else:
                        self.translated += char

                elif char == '"':
                    in_double_quotes = not in_double_quotes
                    self.translated += char

                elif char == "'":
                    in_single_quotes = not in_single_quotes
                    self.translated += char
                
                else:
                    # Normal character, append it and continue
                    self.translated += char

                # Error checking
                if char in ["(", "[", "{"] and not (in_double_quotes or in_single_quotes):
                    bracket_stack.append(
                        {
                            "char": char,
                            "line_number": line_number + 1,     # +1 because the index starts at 0
                            "char_index": char_index + 1        # same here
                        }
                    )

                elif char in [")", "]", "}"] and not (in_double_quotes or in_single_quotes):
                    bracket_mappings: dict = {")": "(", "]": "[", "}": "{"}
                    if len(bracket_stack) == 0:
                        if error_check:
                            raise CurlyPySyntaxError(f"Unmatched '{char}' on line {line_number + 1}, col {char_index + 1}")
                    else:
                        if bracket_stack[-1]["char"] == bracket_mappings[char]:
                            bracket_stack.pop()

                last_useful_char = char
            self.translated += "\n"

            # Line over, we are out of a comment (if we were in one)
            in_comment = False

        # Error checking
        if len(bracket_stack) != 0 and error_check:
            raise CurlyPySyntaxError(f"Unmatched '{bracket_stack[-1]['char']}' on line {bracket_stack[-1]['line_number']}, col {bracket_stack[-1]['char_index']}")

        return self.clean(self.translated, remove_comments) if not output_raw else self.translated

    
    def clean(self, python_code: str, remove_comments: bool = True) -> str:
        """
        Removes empty lines, lines with only whitespace and trailing whitespace from the input code.

        What it does:

        - Removes empty lines and lines with only whitespace
        - Removes trailing whitespace
        - Removes comments from the code (optional)

        Args:
            python_code (str): The Python code to be cleaned.
            remove_comments (bool): Whether to remove comments from the code. Defaults to True.

        Returns:
            str: The cleaned code.
        """

        # Remove comments from the code
        if remove_comments:
            python_code = self.strip_comments(python_code)

        lines: list[str] = []
        for line in python_code.splitlines():
            # Clear all lines with whitespace only, smush every line together
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
