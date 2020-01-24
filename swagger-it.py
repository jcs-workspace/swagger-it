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
from util import *
from info import *


module_name = "swagger-it: Parse your microservice project into a swagger yaml file."
__version__ = "0.0.1"

swagger_identifier = "@swagger"

swagger_ids = [# -- Info ---------------------------------------------------
               "@description", "@version", "@title", "@termsOfService",
               "@contact.email", "@license.name", "@license.url",
               "@host", "@basePath",
               "@tags", "@tags.description", "@tags.externalDocs.description", "@tags.externalDocs.url",
               "@schemes",
               # -- Paths ---------------------------------------------------
               "@router", "@verb",  # For GET, POST, PUT, DELETE, etc.
               "@param",
               "@response", "@success", "@failure",
               # -- Model ---------------------------------------------------
               "@securityDefinitions",
               "@definitions"]

template_file = "./etc/template.yml"

ignore_dir = ['.git', '.vs', '.vscode', '.log', 'node_modules', '__pycache__'];

# Valid programminga language; hence we won't waste our time parsing and
# analyzing the source file we don't want.
valid_ext = ['.c', '.h',
             '.cpp', '.hpp', '.hin', '.cin',
             '.m',
             '.cs', '.js', '.java',
             '.py', '.go', '.rb']
mime_type = ['text/x-c', 'text/x-c',
             'text/x-c++', 'text/x-c++', 'text/x-c++', 'text/x-c++',
             'text/x-c++',
             'text/x-c++', 'application/javascript', 'text/x-java-source',
             'text/x-python', 'text/x-go', 'text/x-ruby']

unique_tags = []   # Tags that can't be repeat.
unique_paths = []  # Paths that can't be repeat.


def getMimeTypeByExtension(ext):
    """Return the mime type string by extension (EXT).

    @param { string } ext : Extension string.
    """
    index = 0
    id = -1
    for vd_ext in valid_ext:
        if vd_ext == ext:
            id = index
            break
        index += 1
        pass
    if id == -1:
        raise ArgumentError('[ERROR] Invalid extension for mime type:', ext)
    return mime_type[id]

def valid_source_file(path):
    """Check if the file PATH valid source file.

    @param { string } path : File path to check valid.
    """
    ext = getFileExtension(path)
    return containInListEqual(ext, valid_ext)

def extract_swagger_identifier(lst_comment):
    """Extract swagger docstring from list of comment/docstring.

    @param { Array } lst_comment : List of comment/docstring.
    """
    valid_swagger_comments = []
    for comment in lst_comment:
        if swagger_identifier in comment.text():
            valid_swagger_comments.append(comment)
            pass
        pass
    return valid_swagger_comments

def form_attribute_list(lst_comment):
    """Turn a list of comments/docstrings to key value pair like JSON.

    @param { typename } lst_comment : List of comment/docstring that contain
    swagger identifier.

    @example
      - @swagger : 2.0
      - @schemes : http, https, ws, wss
      ...
    """
    attr_pair_lst = []
    for comment in lst_comment:
        comment = comment.text().replace('\n', ' ')
        comment = comment.replace(' * ', '')
        attr_lst = comment.split(" @")

        attr = {}

        for attr_line in attr_lst:
            # Form the attribute ID.
            attr_pair = attr_line.split(' ')
            attr_id = '@' + attr_pair.pop(0)
            attr_value = ' '.join(attr_pair)

            if not containInListEqual(attr_id, swagger_ids):
                continue

            attr[attr_id] = attr_value
            pass
        if attr:
            attr_pair_lst.append(attr)
            pass
        pass
    return attr_pair_lst

def fill_swagger_info():
    pass

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

    print("[SWAGGER-IT] Start checking input...")

    if not isFile and not isDir:
        raise ArgumentError('[ERROR] File input error:', input)

    comments = []

    if isFile:  # When is file..
        extension = getFileExtension(input)
        mime_text = getMimeTypeByExtension(extension)
        comments = comment_parser.extract_comments(input, mime=mime_text)
    else:  # When is directory..
        for r, d, f in os.walk(input):
            for file in f:
                filepath = os.path.join(r, file)
                filepath = filepath.replace("\\", "/")
                if not containInList(filepath, ignore_dir) and \
                   valid_source_file(filepath):
                    extension = getFileExtension(filepath)
                    mime_text = getMimeTypeByExtension(extension)
                    new_comments = comment_parser.extract_comments(filepath, mime=mime_text)
                    comments.extend(new_comments)
                    pass
                pass
            pass
        pass

    comments = extract_swagger_identifier(comments)

    print(comments)

    attr_lst = form_attribute_list(comments)

    print(attr_lst)

    # TODO: Outputing .yml file.

    #mkdir_safe(dirname)

    # URL: https://stackoverflow.com/questions/2967194/open-in-python-does-not-create-a-file-if-it-doesnt-exist
    #file = open("", "w+")

    pass

if __name__ == "__main__":
    main()
    pass
