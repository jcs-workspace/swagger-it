# ========================================================================
# $File: info.py $
# $Date: 2020-01-21 20:53:45 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

class SeaggerInfo(object):
    """Swagger API root info."""
    _swagger = "2.0"
    _info = None
    _host = ""
    _basePath = ""
    _tags = []
    _schemes = []
    def __str__(self):
        return f"swagger: \"{_swagger}\"\n" + \
               f"info: \n{_info}" + \
               f"basePath: \"{_basePath}\"" + \
               arrayToString(_tags) + \
               arrayToString(_schemes)
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
        return f"  description: \"{_description}\"\n" + \
               f"  version: \"{_version}\"\n" + \
               f"  title: \"{title}\"\n" + \
               f"  termsOfService: \"{_termsOfService}\"\n" + \
               f"  contact:\n" + \
               f"    email: \"{_contact_email}\"\n" + \
               f"  license:\n" + \
               f"    name: \"{_license_name}\"\n" + \
               f"    url: \"{_license_url}\"\n"
    pass

class TagInfo(object):
    """Tag data structure."""
    _name = ""
    _description = ""
    _externalDocs_description = ""
    _externalDocs_url = ""
    def __str__(self):
        return f"- name: \"{_name}\"\n" + \
               f"  description: \"{_description}\"\n" + \
               f"  externalDocs:\n" + \
               f"    description: \"{_externalDocs_description}\"\n" + \
               f"    url: \"{_externalDocs_url}\"\n"
    pass

class PathInfo(object):
    """Path data structure."""
    _path = ""
    _type = ""  # post? put?
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
    pass

class ResponseInfo(object):
    """Response data structure."""
    _type = ""  # 400, 404, 405, etc.
    _description = ""
    def __str__(self):
        return f"        {_type}:\n" + \
               f"          description: \"{_description}\"\n"
    pass
