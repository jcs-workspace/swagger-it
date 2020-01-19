# ========================================================================
# $File: swagger-it.py $
# $Date: 2020-01-17 16:04:44 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

import os
import platform
import pathlib

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from comment_parser import comment_parser
#from guesslang import Guess

module_name = "swagger-it: Parse your microservice project into a swagger yaml file."
__version__ = "0.0.1"

ignore_dir = ['.git', '.vs', '.vscode', '.log', 'node_modules'];

def containInList(path, lst):
    """Check if each item in LST inside the PATH.

    @param { typename } path : Path for major check.
    @param { typename } lst : List of string that will use to check.
    """
    for item in lst:
        if item in path:
            return True
    return False

class ArgumentError(LookupError):
    """Argument input error."""

def mkdir_safe(path):
    """Make directory if not exists.

    @param { string } path : Directory path.
    """
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def args_input(input):
    """Return the default input path.

    @param { string } input : Default input argument.
    """
    if input is None:
        return os.path.dirname(os.path.abspath(__file__))
    else:
        return input

def main():
    """Program Entry point."""

    version_string = f"%(prog)s {__version__}\n"

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})")

    parser.add_argument("--input", "-i", dest="input",
                        help="Input path, this can be a directory or file.")

    parser.add_argument("--output", "-o", dest="output",
                        help="Output path, this must be a path point to a file.")

    parser.add_argument("--version",
                        action="version",  version=version_string,
                        help="Display version information and dependencies.")

    args = parser.parse_args()

    input = args_input(args.input)
    output = args.output

    if output is None:
        dirname = output   # Set it to None.
        filename = output  # Set it to None.
    else:
        dirname = os.path.dirname(output)    # Target directory path.
        filename = os.path.basename(output)  # Target file to export as swagger yaml.

    isFile = os.path.isfile(input)
    isDir = os.path.isdir(input)

    if not isFile and not isDir:
        raise ArgumentError('File input error:', input)

    print('basename:', filename)
    print('dir:', dirname)

    #mkdir_safe(dirname)

    # URL: https://stackoverflow.com/questions/2967194/open-in-python-does-not-create-a-file-if-it-doesnt-exist
    #file = open("", "w+")

    comments = []

    if isFile:  # When is file..
        comments = comment_parser.extract_comments(input, mime='text/x-c')
    else:  # When is directory..
        for r, d, f in os.walk(input):
            for file in f:
                filepath = os.path.join(r, file)
                filepath = filepath.replace("\\", "/")
                if not containInList(filepath, ignore_dir):
                    new_comments = comment_parser.extract_comments(filepath, mime='text/x-c')
                    comments.extend(new_comments)
                    print('file:', filepath)

    print(comments)


if __name__ == "__main__":
    main()
