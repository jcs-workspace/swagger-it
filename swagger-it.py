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
import re

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
               "@host", "@basePath", "@schemes",
               # -- Tags ---------------------------------------------------
               "@tags", "@tags.description",
               "@tags.externalDocs.description", "@tags.externalDocs.url",
               # -- Paths ---------------------------------------------------
               "@router", "@verb",  # For GET, POST, PUT, DELETE, etc.
               "@summary",
               "@param",
               "@response", "@success", "@failure",
               # -- Model ---------------------------------------------------
               "@securityDefinitions",
               "@definitions"]

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

# The swagger info buffer/file.
# This is the final output result, everything and data will store here.
swagger_info = SeaggerInfo()

exists_tag = None


def get_mime_type_by_extension(ext):
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
    ext = get_file_extension(path)
    return contain_in_list_equal(ext, valid_ext)

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

            if not contain_in_list_equal(attr_id, swagger_ids):
                continue

            attr[attr_id] = attr_value
            pass
        if attr:
            attr_pair_lst.append(attr)
            pass
        pass
    return attr_pair_lst

def fill_info(key, value):
    """Fill in the swagger info by KEY and VALUE.

    @param { string } key : Attribute key.
    @param { string } value : Attribute value.
    """
    # -- Info ---------------------------------------------------
    if key == '@description':
        swagger_info._info._description = value
    elif key == '@version':
        swagger_info._info._version = value
    elif key == '@title':
        swagger_info._info._title = value
    elif key == '@termsOfService':
        swagger_info._info._termsOfService = value
    elif key == '@contact.email':
        swagger_info._info._contact_email = value
    elif key == '@license.name':
        swagger_info._info._license_name = value
    elif key == '@license.url':
        swagger_info._info._license_url = value
    elif key == '@host':
        swagger_info._host = value
    elif key == '@basePath':
        swagger_info._basePath = value
    elif key == '@schemes':
        there_http = re.search('http[^s]', value)
        there_https = re.search('https', value)
        there_ws = re.search('ws[^s]', value)
        there_wss = re.search('wss', value)
        if there_http: swagger_info.add_scheme('http')
        if there_https: swagger_info.add_scheme('https')
        if there_ws: swagger_info.add_scheme('ws')
        if there_wss: swagger_info.add_scheme('wss')
    # -- Tags ---------------------------------------------------
    elif key == '@tags':
        swagger_info.add_tag(value)
        pass
    elif key == '@tags.description':
        if exists_tag:
            print('[WARNING] Define tag description without tag defined.')
        else:
            exists_tag._description = value
            pass
        pass
    elif key == '@tags.externalDocs.description':
        if exists_tag:
            print('[WARNING] Define tag external document description without tag defined.')
        else:
            exists_tag._externalDocs_description = value
            pass
        pass
    elif key == '@tags.externalDocs.url':
        if exists_tag:
            print('[WARNING] Define tag external document URL without tag defined.')
        else:
            exists_tag._externalDocs_url = value
            pass
        pass
    # -- Paths ---------------------------------------------------
    elif key == '@summary':
        pass
    elif key == '@param':
        pass
    elif key == '@response':
        pass
    elif key == '@success':
        pass
    elif key == '@failure':
        pass
    # -- Model ---------------------------------------------------
    elif key == '@securityDefinitions':
        pass
    elif key == '@definitions':
        pass
    else:
        print('[WARNING] Use key not found:', key)
        pass
    pass

def fill_swagger_info(attr_lst):
    """Fill the swagger information by attribute list (ATTR_LST).

    @param { Array } attr_lst : List of attributes.
    """
    global exists_tag
    for attr in attr_lst:
        tag_name = dict_get_value(attr, '@tags')
        exists_tag = swagger_info.get_tag(tag_name)
        for key in attr:
            fill_info(key, attr[key])
            pass
        pass
    pass

def form_swagger_buffer(comments):
    """Form the swagger buffer.

    @param { Array } comments : List of comments or properly swagger docstrings.
    """
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
        extension = get_file_extension(input)
        mime_text = get_mime_type_by_extension(extension)
        comments = comment_parser.extract_comments(input, mime=mime_text)
    else:  # When is directory..
        for r, d, f in os.walk(input):
            for file in f:
                filepath = os.path.join(r, file)
                filepath = filepath.replace("\\", "/")
                if not contain_in_list(filepath, ignore_dir) and \
                   valid_source_file(filepath):
                    extension = get_file_extension(filepath)
                    mime_text = get_mime_type_by_extension(extension)
                    new_comments = comment_parser.extract_comments(filepath, mime=mime_text)
                    comments.extend(new_comments)
                    pass
                pass
            pass
        pass

    comments = extract_swagger_identifier(comments)
    attr_lst = form_attribute_list(comments)

    print(comments)

    fill_swagger_info(attr_lst)

    print(swagger_info)

    # TODO: Outputing .yml file.

    #mkdir_safe(dirname)

    # URL: https://stackoverflow.com/questions/2967194/open-in-python-does-not-create-a-file-if-it-doesnt-exist
    #file = open("", "w+")

    pass

if __name__ == "__main__":
    main()
    pass
