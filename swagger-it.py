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
#from util import *
#from info import *


module_name = "swagger-it: Parse your microservice project into a swagger yaml file."
__version__ = "0.0.1"

swagger_identifier = "@swagger"

swagger_ids = ["@description", "@version", "@title", "@termsOfService",
               "@contact.email", "@license.name", "@license.url",
               "@host", "@basePath",
               "@tags", "@tags.description", "@tags.externalDocs.description", "@tags.externalDocs.url",
               "@schemes",
               "@securityDefinitions",
               "@definitions"]

template_file = "./etc/template.yml"

ignore_dir = ['.git', '.vs', '.vscode', '.log', 'node_modules', '__pycache__'];

unique_tags = []   # Tags that can't be repeat.
unique_paths = []  # Paths that can't be repeat.


def extract_swagger_identifier(lst_comments):
    """Extract swagger docstring from list of comment.

    @param { Array } lst_comments : List of comment that contain swagger identifier.
    """
    valid_swagger_comments = []
    for comment in lst_comments:
        if swagger_identifier in comment.text():
            valid_swagger_comments.append(comment)
            pass
        pass
    return valid_swagger_comments

def form_swagger_buffer(comments):
    """Form the swagger buffer.

    @param { Array } comments : List of comments or properly swagger docstrings.
    """
    with open(template_file, 'r') as file:
        template_buffer = file.read()
        pass
    for comment in comments:

        pass
    return template_buffer

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
        pass

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
                    pass
                pass
            pass
        pass

    comments = extract_swagger_identifier(comments)

    print(comments)
    pass

if __name__ == "__main__":
    main()
    pass
