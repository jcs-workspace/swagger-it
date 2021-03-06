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
from util import *
from info import *


module_name = "swagger-it: Parse your microservice project into a swagger yaml file."
__version__ = "0.0.1"

swagger_identifier = "@swagger"

swagger_ids = [# -- Info ---------------------------------------------------
               "@description", "@version", "@title", "@termsOfService",
               "@contact.email", "@license.name", "@license.url",
               "@host", "@basePath", "@schemes",
               "@externalDocs.description", "@externalDocs.url",
               # -- Tags ---------------------------------------------------
               "@tags",  # Followed by name.
               "@tags.description",
               "@tags.externalDocs.description", "@tags.externalDocs.url",
               # -- Paths --------------------------------------------------
               "@router",  # Followed by name.
               "@verb",  # For GET, POST, PUT, DELETE, etc.
               "@summary", "@description",
               "@operationId",
               "@param",
               "@response", "@success", "@failure",
               "@security",
               # -- Security Definitions -----------------------------------
               "@securityDefinitions",  # Followed by name.
               "@name",
               "@type", "@authorizationUrl", "@tokenUrl", "@flow", "@in", "@required",
               "@scope.admin", "@scope.read", "@scope.write",
               # -- Definitions --------------------------------------------
               "@def",  # Followed by name.
               "@type",
               "@property.description", "@property.type", "@property.format"]

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
exists_path = None


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

            attr[attr_id] = attr_value.strip()
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
        if exists_path:  # @router exists.
            swagger_info.get_path(exists_path)._description = value
            pass
        else:
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
    elif key == 'externalDocs.description':
        swagger_info._externalDocs_description = value
    elif key == 'externalDocs.url':
        swagger_info._externalDocs_url = value
    elif key == '@externalDocs.description':
        swagger_info._externalDocs_description = value
    elif key == '@externalDocs.url':
        swagger_info._externalDocs_url = value
    # -- Tags ---------------------------------------------------
    elif key == '@tags':
        swagger_info.get_tag(value)  # Create one on it's own
        if exists_path:
            swagger_info.get_path(exists_path)._tags = value
        pass
    elif key == '@tags.description':
        if not exists_tag:
            warn_exists('@tags.description', '@tags')
        else:
            swagger_info.get_tag(exists_tag)._description = value
    elif key == '@tags.externalDocs.description':
        if not exists_tag:
            warn_exists('@tags.externalDocs.description', '@tags')
        else:
            swagger_info.get_tag(exists_tag)._externalDocs_description = value
    elif key == '@tags.externalDocs.url':
        if not exists_tag:
            warn_exists('@tags.externalDocs.url', '@tags')
        else:
            swagger_info.get_tag(exists_tag)._externalDocs_url = value
    # -- Paths ---------------------------------------------------
    elif key == '@router':
        path_info = swagger_info.get_path(value)  # Create one on it's own

        # Parse parameter from router.
        pattern = re.compile(r'{\w*}')  # Find all parameters between { }.
        matches = pattern.finditer(value)

        for match in matches:
            match_val = match.group()
            end_pt = len(match_val) - 1
            path_info.get_param(match_val[1:end_pt])
        pass

    elif key == '@verb':
        if not exists_path:
            warn_exists('@verb', '@router')
        else:
            swagger_info.get_path(exists_path)._verb = value
    elif key == '@summary':
        if not exists_path:
            warn_exists('@summary', '@router')
        else:
            swagger_info.get_path(exists_path)._summary = value
    elif key == '@operationId':
        if not exists_path:
            warn_exists('@operationId', '@router')
        else:
            swagger_info.get_path(exists_path)._operationId = value
    elif key == '@param':
        # TODO: parse `param` description.
        keywords = value.split()

        param_name = keywords[0]  # First is the name of variable.

        param = swagger_info.get_path(exists_path).get_param(param_name)

        for kw in keywords:
            current_type = contain_in_list_equal(kw, PARAM_TYPES)
            if current_type:
                param.set_type(current_type)
                break
            pass
        for kw in keywords:
            current_in = contain_in_list_equal(kw, PARAM_INS)
            if current_in:
                param.set_in(current_in)
                break
            pass
        for kw in keywords:
            current_req = contain_in_list_equal(kw, PARAM_REQUIRED)
            if current_req:
                param.set_required(current_req)
                break
            pass

        pass
    elif key == '@response' or key == '@success' or key == '@failure':
        if not exists_path:
            warn_exists('@response / @success / @failure', '@router')
        else:
            fmt_val_lst = value.split(' ')
            current_path = swagger_info.get_path(exists_path)

            # This is where I parse `@response` format.
            res_id = safe_get_value(fmt_val_lst, 0)
            res_type_or_ref = safe_get_value(fmt_val_lst, 1)
            res_desc = safe_get_value(fmt_val_lst, 2)

            new_res = current_path.get_response(res_id)
            new_res._description = res_desc
            new_res._type_or_ref = res_type_or_ref
        pass
    elif key == '@security':
        pass
    # -- Security Definitions -----------------------------------
    elif key == '@securityDefinitions':
        pass
    elif key == '@securityDefinitions.type':
        pass
    elif key == '@securityDefinitions.flow':
        pass
    elif key == '@authorizationUrl':
        pass
    elif key == '@tokenUrl':
        pass
    elif key == '@scope.admin':
        pass
    elif key == '@scope.read':
        pass
    elif key == '@scope.write':
        pass
    # -- Definitions --------------------------------------------
    elif key == '@def':
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
    global exists_path
    for attr in attr_lst:
        exists_tag = dict_get_value(attr, '@tags')
        exists_path = dict_get_value(attr, '@router')
        for key in attr:
            fill_info(key, attr[key])
            pass
        pass
    pass

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

    print("[SWAGGER-IT] Start checking input:::")

    if not isFile and not isDir:
        raise ArgumentError('[ERROR] File input error:', input)

    print("[SWAGGER-IT] Start checking output:::")

    if not dirname and not filename:
        raise ArgumentError('[ERROR] File output error:', output)

    print("[SWAGGER-IT] Parsing comments and docstrings:::")

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

    print("[SWAGGER-IT] Filling swagger informations:::")

    fill_swagger_info(attr_lst)

    print(swagger_info)

    mkdir_safe(dirname)  # Ensure the path exists.

    file = open(output, "w+")
    file.write(str(swagger_info))
    file.close()

    print("[SWAGGER-IT] Done generate the file:::")
    pass

if __name__ == "__main__":
    main()
    pass
