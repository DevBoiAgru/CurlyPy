import sys
import argparse
import subprocess
import os

from curlypy.curlypy import CurlyPyTranslator


def main():
    parser = argparse.ArgumentParser(description="Translate and run python code with braces")

    parser.add_argument("filename", type=str, help="The filename to translate.")
    parser.add_argument("--output", type=str, help="The output filename. Defaults to <filename>.py")
    parser.add_argument("--run", action="store_true", help="Set this flag if you want to run the translated code directly after translating.")
    parser.add_argument("--comments", action="store_true", help="Set this flag if you want to keep comments in the translated code.")
    parser.add_argument("--force", action="store_true", help="Set this flag if you want to force the translation. i.e. dont perform any checks. Can output non working code. Defaults to False.")
    parser.add_argument("--delete", action="store_true", help="Set this flag if you want to delete the translated file after running it.")

    args = parser.parse_args()

    # Translating
    translator = CurlyPyTranslator()

    try:
        with open(args.filename, "r") as f:
            original_code = f.read()
            translated: str = translator.translate(original_code, force_translate=args.force)

            output_file = (args.output if args.output else f"{args.filename}.py").replace(".cpy", "")
            with open(output_file, "w") as f:
                f.write(translated)

            if args.run:
                # Run the translated code
                subprocess.Popen(["python", output_file]).wait()

                if args.delete:
                    # Remove the translated file
                    os.remove(output_file)

    except FileNotFoundError:
        print(f"File '{args.filename}' not found", file=sys.stderr)
        sys.exit(1)




main()