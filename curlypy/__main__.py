import sys
from curlypy.curlypy import CurlyPyTranslator

brython_translator = CurlyPyTranslator(filename=sys.argv[1])
with open(sys.argv[2], "+w") as out:
    out.write(
        brython_translator.translate_file(remove_comments=False)
    )