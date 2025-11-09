# CurlyPy: Python with Brackets

**CurlyPy** is a preprocessor that translates Python code written using curly braces (`{}`) into standard Python, making indentation obsolete. It provides the flexibility to use semicolons (`;`) as optional statement separators, making Python syntax more familiar to developers accustomed to languages like C, Java, or JavaScript.

With CurlyPy, you can write Python code using braces to define code blocks, eliminating the need for indentation while still retaining Python's powerful features.

## Key Features

- **Curly Braces for Code Blocks**: Use `{}` to denote the start and end of code blocks, removing the need for indentation.
- **Semi-Mandatory Semicolons**: Semicolons (`;`) are supported as optional separators between statements, but they are still not strictly required after every statement. They will, however, be required if you are writing multiple instructions in the same line.
- **Flexible Syntax**: Write Python code with a more structured format, closer to languages like C, Java, or JavaScript, while keeping all the strengths of Python.
- **Compatible with Python**: CurlyPy preprocesses your code into standard Python, so it can be executed by any Python interpreter.
- **Dictionary and Set Types**: The standard Python dictionary and set types are available in CurlyPy, using type hints.
- **C Style multi-line comments**: CurlyPy adds support for the `/* comment */` styled block comments, for people familiar with C-like languages.
- **Syntax highlighting**: A VS Code extension to get you up and running with basic syntax highlighting and a few handy snippets, check it out here: https://github.com/DevBoiAgru/curlypy-vscode-extension/

Valid CurlyPy syntax:

```python
/* Dictionaries and sets are defined using type hints */
dictionary_test: dict[str, str] = {
   "foo":"bar",
   "baz":{
      "qux":"quux"
   }
}
set_test: set[str] = {"foo", "bar", "baz"}
print(dictionary_test["foo"], set_test)
```

CurlyPy makes even this syntax possible!

```python
def check_even_odd(num) { print(f"{num} is {'even' if num % 2 == 0 else 'odd'};"); }; check_even_odd(10); check_even_odd(7);
```

## Installation

**Install from PyPI:**

```bash
pip install curlypy
```

## Usage

Once you have CurlyPy installed, you can preprocess your Python files written with curly braces and optional semicolons into standard Python.

### Command line usage:

```bash
# Example usage
>> curlypy path/to/curlypy/file

# To get help
>> curlypy -h
usage: curlypy [-h] [--output OUTPUT] [--norun] [--force] [--keep] filename ...

Translate and run python code with braces

positional arguments:
  filename         The filename to translate.
  args             Arguments to pass to the translated code.

options:
  -h, --help       show this help message and exit
  --output OUTPUT  The output filename. Defaults to _curlypy_<filename>.py
  --norun          Set this flag if you dont want to run the translated code directly after translating.
  --force          Set this flag if you want to force the translation. i.e. dont perform any checks. Can output non working code. Defaults to False.
  --keep           Set this flag if you want to keep the translated file after running it.
```

### Module usage:

```python
# some_file.py
from curlypy import CurlyPyTranslator

translator = CurlyPyTranslator(filename="curlypython.curlypy")
translated_code: str = translator.translate()

with open("translated.py", "+w") as out:
    out.write(translated_code)
# Then run translated.py using python

```

CurlyPy will convert your code with brackets into traditional Python with correct indentation and block structures.

### Example

Here's how Python code with curly braces and semicolons looks with CurlyPy:

```python
def HelloWorld(name: str) {
	if name {
		print (f"Hello {name}!");
	}
	else {
		print ("Hello World!");
	}
}
```

With curlypy, it will be converted into regular Python:

```python
def HelloWorld(name: str) :
   if name :
      print (f"Hello {name}!")
   else :
      print ("Hello World!")
```

## Check out the VS Code extension for a smoother experience

[VS Code extension](https://github.com/DevBoiAgru/curlypy-vscode-extension/),
Ready for you to install

## Why CurlyPy?

Python's indentation-based syntax is great for readability but may feel unfamiliar to developers used to brace-based languages like C, Java, or JavaScript. CurlyPy gives you the freedom to write Python code with curly braces, making it easier for those developers to transition to Python without abandoning the structured code block formatting they're used to.

CurlyPy doesn't take away Python's flexibility—if you love type hints and it's strong typing, you can keep using them as is. CurlyPy opens up new possibilities for those who prefer braces.

CurlyPy:

```python
/* For loop
which prints
FizzBuzz */
for n in range(10){
    if n % 3 == 0 and n % 5 == 0 {
        print("FizzBuzz")
	}
    elif n % 3 == 0 {
		print("Fizz")
	}
    elif n % 5 == 0 {
		print("Buzz")
	}
    else{
        print(n)
	}
}
```

Translated Python:

```python
# For loop
for n in range(10):
   if n % 3 == 0 and n % 5 == 0 :
      print("FizzBuzz")
   elif n % 3 == 0 :
      print("Fizz")
   elif n % 5 == 0 :
      print("Buzz")
   else:
      print(n)
```

## Error Checking

CurlyPy performs a number of checks before translating your code, to ensure it runs correctly after translation.

```
simple_int: int = 42
simple_str: str = 'hello'
simple_dict: dict[str, dict] = {'a': {1:2, 'b': {2:3}}
simple_float: float = 3.14
simple_bool: bool = True
```

raises: curlypy.errors.CurlyPySyntaxError: Unmatched '{' on line 3, col 32

## Upcoming improvements

- Advanced preprocessing features
- Advanced error checking
- Possibly a new name
- More in depth documentation

## Contributing

Contributions are welcome! If you want to contribute to CurlyPy or report an issue, please feel free to open an issue or submit a pull request.

### If you run into an issue or an edge case, please open an issue and help us improve CurlyPy!

### Steps to Contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Submit a pull request with a clear description of the change

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy writing Python with the structure and familiarity of braces with **CurlyPy**!
