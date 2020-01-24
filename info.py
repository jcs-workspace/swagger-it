# ========================================================================
# $File: info.py $
# $Date: 2020-01-21 20:53:45 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

from util import *

class ResponseInfo(object):
    """Response data structure."""
    _type = ""  # 400, 404, 405, etc.
    _description = ""

    def __str__(self):
        return f"        {self._type}:\n" + \
               f"          description: \"{self._description}\"\n"
    pass

class PathInfo(object):
    """Path data structure."""
    _path = ""
    _verb = ""  # post? put?
    _tags = ""
    _summary = ""
    _description = ""
    _operationId = ""
    _consumes = []
    _produces = []
    _parameters_in = ""
    _parameters_name = ""
    _parameters_description = ""
    _parameters_required = True
    _parameters_schema_ref = ""
    _responses = []

    def __str__(self):
        return f"  {self._self}:\n" + \
               f"    {self._vard}:\n" + \
               f"      tags:\n" + \
               f"      - \"{self._tags}\"\n" + \
               f"      summary: {self._summary}\n" + \
               f"      description: {self._description}\n" + \
               f"      operationId: {self._operationId}\n"
    pass

class TagInfo(object):
    """Tag data structure."""
    _name = ""
    _description = ""
    _externalDocs_description = ""
    _externalDocs_url = ""

    def __str__(self):
        return f"- name: \"{self._name}\"\n" + \
               f"  description: \"{self._description}\"\n" + \
               f"  externalDocs:\n" + \
               f"    description: \"{self._externalDocs_description}\"\n" + \
               f"    url: \"{self._externalDocs_url}\"\n"
    pass

class APIInfo(object):
    """Swagger api info section."""
    _description = ""
    _version = ""
    _title = ""
    _termsOfService = ""
    _contact_email = ""
    _license_name = ""
    _license_url = ""

    def __str__(self):
        return f"  description: \"{self._description}\"\n" + \
               f"  version: \"{self._version}\"\n" + \
               f"  title: \"{self._title}\"\n" + \
               f"  termsOfService: \"{self._termsOfService}\"\n" + \
               f"  contact:\n" + \
               f"    email: \"{self._contact_email}\"\n" + \
               f"  license:\n" + \
               f"    name: \"{self._license_name}\"\n" + \
               f"    url: \"{self._license_url}\"\n"
    pass

class SeaggerInfo(object):
    """Swagger API root info."""
    _swagger = "2.0"
    _info = APIInfo()
    _host = ""
    _basePath = ""
    _tags = []
    _schemes = []
    _paths = []

    def __str__(self):
        return f"swagger: \"{self._swagger}\"\n" + \
               f"info:\n {self._info}" + \
               f"host: \"{self._host}\"\n" + \
               f"basePath: \"{self._basePath}\"\n" + \
               len_zero_string(self._tags, 'tags:\n') + \
               array_to_string(self._tags) + \
               len_zero_string(self._schemes, 'schemes:\n') + \
               array_to_string(self._schemes) + \
               len_zero_string(self._paths, 'tags:\n') + \
               array_to_string(self._paths)

    def add_scheme(self, option):
        """Scheme defined in Swagger/OpenAPI."""
        if not option is "https" and not option is "http" and \
            not option is "ws" and not option is "wss":
            print('[WARNING] Wrong scheme option:', option)
            return
        self._schemes.append(f"- {option}\n")
        pass

    def add_tag(self, tag_name):
        """Add tag by new TAG_NAME.

        @param { string } tag_name : Tag name.
        """
        tag = TagInfo()
        tag._name = tag_name
        self._tags.append(tag)
        return tag

    def get_tag(self, tag_name):
        """Get tag by TAG_NAME.
        If not found, we create a new one."""
        for tag in self._tags:
            if tag._name == tag_name:
                return tag
            pass
        new_tag = self.add_tag(tag_name)
        return new_tag
    pass
