import sys
import argparse
import os

from curlypy import CurlyPyTranslator


def main():
    argparser = argparse.ArgumentParser(
        description="Translate and run python code with braces"
    )

    argparser.add_argument("filename", type=str, help="The filename to translate.")
    argparser.add_argument(
        "--output",
        type=str,
        help="The output filename. Defaults to _curlypy_<filename>.py",
    )
    argparser.add_argument(
        "--norun",
        action="store_true",
        help="Set this flag if you dont want to run the translated code directly after translating.",
    )
    argparser.add_argument(
        "--force",
        action="store_true",
        help="Set this flag if you want to force the translation. i.e. dont perform any checks. Can output non working code. Defaults to False.",
    )
    argparser.add_argument(
        "--keep",
        action="store_true",
        help="Set this flag if you want to keep the translated file after running it.",
    )
    argparser.add_argument(
        "args",
        type=str,
        help="Arguments to pass to the translated code.",
        nargs=argparse.REMAINDER,
    )

    args = argparser.parse_args()

    # Translating
    translator = CurlyPyTranslator()

    try:
        with open(args.filename, "r") as f:
            original_code = f.read()
            translated: str = translator.translate(
                original_code, error_check=not args.force
            )

            if args.keep:
                output_file = args.output if args.output else f"{args.filename[:-4]}.py"
            else:
                output_file = (
                    args.output if args.output else f"_curlypy_{args.filename[:-4]}.py"
                )

            with open(output_file, "w") as f:
                f.write(translated)

            if not args.norun:
                # Run the translated code
                os.system(f"python {output_file} {' '.join(args.args)}")

            if not args.keep:
                # Remove the translated file
                os.remove(output_file)

    except FileNotFoundError:
        print(f"File '{args.filename}' not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
