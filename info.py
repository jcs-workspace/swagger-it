# ========================================================================
# $File: info.py $
# $Date: 2020-01-21 20:53:45 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

from util import *

class PropertyInfo(object):
    """Property data structure."""
    _name = ""
    _type = ""
    _description = ""
    _format = ""
    _default = None  # None, True or False

    def __str__(self):
        return f"      {self._name}:\n" + \
               none_string(self._description,
               f"        description: \"{self._type}\"\n") + \
               none_string(self._type,
               f"        type: \"{self._type}\"\n") + \
               none_string(self._format,
               f"        format: \"{self._format}\"\n") + \
               none_string(self._default,
               f"        default: \"{self._default}\"\n")
        pass

class DefinitionInfo(object):
    """Definition data structure."""
    _name = ""  # Variable name.
    _type = ""
    _properties = []

    def __str__(self):
        return f"  {self._name}:\n" + \
               f"    type: {self._type}" + \
               len_zero_string(self._properties, 'properties:\n') + \
               array_to_string(self._properties) + \
               f"    xml:\n" + \
               f"      name: {self._name}"
    pass

class SecurityDefinitionInfo(object):
    """Security definition data structure."""
    _id = ""
    _type = ""
    _name = ""
    _flow = ""
    _authorizationUrl = ""
    _scopes = []  # TODO:  ..
    _in = ""

    def __str__(self):
        return f"  {self._id}:\n" + \
               f"    type: \"{self._type}\"\n" + \
               f"    name: \"{self._name}\"\n" + \
               f"    authorizationUrl: \"{self._authorizationUrl}\"\n" + \
               f"    flow: \"{self._flow}\"\n" + \
               f"    in: \"{self._in}\"\n"
    pass

class ResponseInfo(object):
    """Response data structure."""
    _id = ""  # 400, 404, 405, etc.
    _description = ""
    _type_or_ref = ""

    def type_valid(self):
        """Check _type_or_ref a valid value."""
        return self._type_or_ref == 'array' or \
               self._type_or_ref == 'boolean' or \
               self._type_or_ref == 'integer' or \
               self._type_or_ref == 'number' or \
               self._type_or_ref == 'object' or \
               self._type_or_ref == 'string' or \
               self._type_or_ref == 'file'

    def __str__(self):
        return f"        {self._id}:\n" + \
               f"          description: \"{self._description}\"\n" + \
               none_string(self._type_or_ref,
               "          schema:\n" + \
               none_string(self.type_valid(),
               f"           type: \"{self._type_or_ref}\"\n") + \
               none_string(not self.type_valid(),
               f"           $ref: \"{self._type_or_ref}\"\n"))
    pass

class ParameterInfo(object):
    """Parameter data structure."""
    _name = ""
    _in = ""
    _description = ""
    _required = None
    _ref = ""

    def __str__(self):
        return f"      - name: \"{self._name}\"\n" + \
               f"        in: \"{self._in}\"\n" + \
               none_string(self._description,
               f"        description: \"{self._description}\"\n") + \
               none_string(self._required,
               f"        required: {self._required}\n") + \
               f"        schema:\n" + \
               f"          $ref: \"{self._ref}\"\n"
    pass

class PathInfo(object):
    """Path data structure."""
    _path = ""  # For @router keyword.
    _verb = ""  # post? put?
    _tags = ""
    _summary = ""
    _description = ""
    _operationId = ""
    _consumes = []
    _produces = []
    _parameters = []
    _responses = []
    _security = []

    def __str__(self):
        return f"  {self._path}:\n" + \
               f"    {self._verb}:\n" + \
               f"      tags:\n" + \
               f"      - \"{self._tags}\"\n" + \
               none_string(self._summary,
               f"      summary: \"{self._summary}\"\n") + \
               none_string(self._description,
               f"      description: \"{self._description}\"\n") + \
               none_string(self._operationId,
               f"      operationId: \"{self._operationId}\"\n") + \
               len_zero_string(self._consumes,
               '      consumes:\n') + \
               array_to_string(self._consumes) + \
               len_zero_string(self._produces,
               '      produces:\n') + \
               array_to_string(self._produces) + \
               len_zero_string(self._produces,
               '      parameters:\n') + \
               array_to_string(self._parameters) + \
               len_zero_string(self._responses,
               '      responses:\n') + \
               array_to_string(self._responses) + \
               len_zero_string(self._security,
               '      security:\n') + \
               array_to_string(self._security)

    def add_consume(self, name):
        """Add a new consume."""
        self._consumes.append("- {name}\n")
        pass

    def add_produce(self, name):
        """Add a new produce."""
        self._produces.append("- {name}\n")
        pass

    def add_response(self, id):
        """Add a new response."""
        new_res = ResponseInfo()
        new_res._id = id
        self._responses.append(new_res)
        return new_res

    def get_response(self, id):
        """Return a response data by ID.
        If not found, create a new one."""
        if not id:
            return None
        for response in self._responses:
            if response._id == id:
                return response
            pass
        new_res = self.add_response(id)
        return new_res

    def get_param(self, name):
        """Add a new parameter."""
        # TODO: ..
        pass
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
               none_string(self._contact_email,
               f"  contact:\n" + \
               f"    email: \"{self._contact_email}\"\n") + \
               none_string(self._license_name is "" and self._license_url is "",
               f"  license:\n" + \
               f"    name: \"{self._license_name}\"\n" + \
               f"    url: \"{self._license_url}\"\n")
    pass

class SeaggerInfo(object):
    """Swagger API root info."""
    _swagger = "2.0"
    _info = APIInfo()  # Only one instance.
    _host = ""
    _basePath = ""
    _tags = []
    _schemes = []
    _paths = []
    _securityDefinitions = []
    _definitions = []
    _externalDocs_description = ""
    _externalDocs_url = ""

    def __str__(self):
        return f"swagger: \"{self._swagger}\"\n" + \
               f"info:\n{self._info}" + \
               f"host: \"{self._host}\"\n" + \
               f"basePath: \"{self._basePath}\"\n" + \
               len_zero_string(self._tags, 'tags:\n') + \
               array_to_string(self._tags) + \
               len_zero_string(self._schemes, 'schemes:\n') + \
               array_to_string(self._schemes) + \
               len_zero_string(self._paths, 'paths:\n') + \
               array_to_string(self._paths) + \
               "externalDocs:\n" + \
               f"  description: \"{self._externalDocs_description}\"\n" + \
               f"  url: \"{self._externalDocs_url}\""

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

        @param { string } tag_name : Name of the tag.
        """
        tag = TagInfo()
        tag._name = tag_name
        self._tags.append(tag)
        return tag

    def get_tag(self, tag_name):
        """Get tag by TAG_NAME.
        If not found, we create a new one."""
        if not tag_name:
            return None
        for tag in self._tags:
            if tag._name == tag_name:
                return tag
            pass
        new_tag = self.add_tag(tag_name)
        return new_tag

    def add_path(self, path_name):
        """Add path by new PATH_NAME.

        @param { string } path_name : Name of the path/route.
        """
        path = PathInfo()
        path._path = path_name
        self._paths.append(path)
        return path

    def get_path(self, path_name):
        """Get path by PATH_NAME.
        If not found, we create a new one."""
        if not path_name:
            return None
        for path in self._paths:
            if path._path == path_name:
                return path
            pass
        new_path = self.add_path(path_name)
        return new_path

    def add_def(self, def_name):
        """"Add one definition by DEF_NAME."""
        defi = DefinitionInfo()
        defi._name = def_name
        self._definitions.append(defi)
        return defi

    def get_def(self, def_name):
        """Get definition by DEF_NAME.

        @param { string } def_name : Name of the definition.
        """
        if not def_name:
            return None
        for defi in self._definitions:
            if defi._name == def_name:
                return defi
            pass
        new_defi = self.add_def(def_name)
        return new_defi
    pass
