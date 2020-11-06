import glob
import os
import pyquery
import lxml
import inspect
import contextlib
import copy
import re

from .compat import IS_PY2


def match(xml, tag, attrib={}):
    """ Matches whether the XML has the specified tag and attributes.

    :return: True if there is a match otherwise False
    """

    if tag != xml.tag:
        return False

    for key in attrib:
        try:
            if xml.attrib[key] != attrib[key]:
                return False
        except KeyError:
            return False

    return True


def parse_using_type(definition):
    """ Doxygen does not handle using statements the way we would like
    so we extract the type from it
    """

    parser = re.compile(r"""
        using              # Match 'using'
        \s+                # Match one or more spaces
        (?P<name>          # Match and group ("name")
            [\w:<>_&*()]+  #  Match on or more characters
        )                  # End group
        \s+                # Match one or more spaces
        =                  # Match an equal operator
        \s+                # Match one or more spaces
        (?P<type>          # Match and group ("type")
            [\w:<>_&*()]+  #  Match on or more characters
        )                  # End group
        """, re.VERBOSE)

    result = parser.match(definition)

    if result is None:
        raise RuntimeError(
            "Failed to parse using statement {}".format(definition))

    return result.group('type')


def replace_with(replace, data):
    """ Replaces values in the data using the mapping provided in the
        replace dict.

    :param replace: Dictionary where all keys found in the input should
        be replaced with the corresponding value.
    :param data: Dictionary of list of values that should be replaced.

    return The updated copy with values replaced.
    """

    def _replace(value):
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = _replace(v)

            return value

        if isinstance(value, list):
            return [_replace(v) for v in value]

        if value in replace:
            return replace[value]
        else:
            return value

    data = copy.deepcopy(data)

    return _replace(data)


class ParserFunction(object):

    def __init__(self, function, tag, attrib):
        self.function = function
        self.tag = tag
        self.attrib = attrib if attrib else {}

    @property
    def score(self):
        """ The score is how "specilized" the parser function is.

        If can_parse returns True the score can be used to select
        one parser over another.

        E.g. say we have two parsers:

        1. For "compounddef" no attributes
        2. For "compounddef" and kind "class"

        Then if both returns True for can_parse then 2 will be
        choosen since it has a score of 1 and the other has a score
        of 0.
        """

        return len(self.attrib)

    def __repr__(self):
        return ("<{} tag='{}', attrib='{}'>".format(
            self.__class__.__name__, self.tag, self.attrib))


class DoxygenParser(object):

    # Default parsers
    default_parsers = []

    def __init__(self, doxygen_path, location_mapper, patch_api, log):
        """ Create a new DoxygenParser

        :param doxygen_path: The path to where the Doxygen XML is
            located.
        :param location_mapper: Takes paths provided by Doxygen and maps it
            to relative paths for include and within the project
        :param patch_api: Set of patches to apply to the API after parsing the
            Doxygen XML.
        :param log: Log object
        """
        self.doxygen_path = doxygen_path
        self.location_mapper = location_mapper
        self.patch_api = patch_api
        self.log = log

        # The parser functions registered
        self.parsers = DoxygenParser.default_parsers

        # Scope variable used to track the C++ scope of member
        # functions etc.
        self.scope = None

        # Doxygen has its own internal id mapping, these ids need
        # to be translated to our unique-names. We do this as the
        # last step in the parsing. We track the id to unique-name
        # mapping with the following dict
        self.id_mapping = {}

    @contextlib.contextmanager
    def set_scope(self, scope):
        assert self.scope is None

        self.scope = scope
        yield
        self.scope = None

    def parse_index(self):
        """ Start parsing from the doxygen index.xml file

        :return: API dictionary
        """

        # Find the index XML file
        index_path = os.path.join(self.doxygen_path, 'index.xml')

        assert(os.path.isfile(index_path))

        index_xml = lxml.etree.parse(source=index_path)

        api = {}

        # Iterate thought the "compound" elements of the Doxygen index.xml
        for compound in index_xml.findall('compound'):

            compound_api = self.parse_element(xml=compound)

            api.update(compound_api)

        api = replace_with(replace=self.id_mapping, data=api)

        def apply_patch(selector, key, value):
            api[selector][key] = value

        for patch in self.patch_api:
            apply_patch(**patch)

        return api

    def parse_element(self, xml):
        """ Parse an XML element """

        parser = self._find_in_list(xml=xml)

        # Inject needed arguments
        args = {'xml': xml}

        if IS_PY2:
            require_arguments = inspect.getargspec(parser.function)[0]

        else:
            require_arguments = inspect.getfullargspec(parser.function)[0]

        for argument in require_arguments:
            if argument == "parser":
                args["parser"] = self
            elif argument == "log":
                args["log"] = self.log
            elif argument == "location_mapper":
                args["location_mapper"] = self.location_mapper
            elif argument == "scope":
                args["scope"] = self.scope
            elif argument == "xml":
                continue
            else:
                raise RuntimeError("Not injectable arg {}".format(argument))

        return parser.function(**args)

    def supports(self, xml):

        try:
            self._find_in_list(tag=xml.tag, attrib=xml.attrib)
        except RuntimeError:
            return False
        else:
            return True

    def _find_in_list(self, xml):
        """ Find the parser function for a specific XML element.

        :param xml: The XML element
        :return: A ParserFunction object
        """

        candidate = None

        for parser in self.parsers:

            if match(xml=xml, tag=parser.tag, attrib=parser.attrib):

                if candidate is None:
                    candidate = parser
                elif candidate.score < parser.score:
                    candidate = parser
                elif candidate.score == parser.score:
                    raise RuntimeError("Two ambigious parsers")
                else:
                    continue

        if candidate is None:
            raise RuntimeError(
                "No parser for tag {} attrib {}\nCandidates are: {}".format(
                    xml.tag, xml.attrib, self.parsers))

        return candidate

    @staticmethod
    def register(tag, attrib=None):
        """ Decorator for registering parser functions.

        The decorator will take an XML tag and optional attributes and
        use that to register a parser function.
        """
        def _register(function):

            for parser in DoxygenParser.default_parsers:

                if parser.tag != tag:
                    continue

                if parser.attrib != attrib:
                    continue

                raise RuntimeError("Parser {} {} Already exists".format(
                    tag, attrib))

            else:
                # If the parser does not already exist we add it
                parser = ParserFunction(
                    function=function, tag=tag, attrib=attrib)

                DoxygenParser.default_parsers.append(parser)

            return function

        return _register


@DoxygenParser.register(tag='compound')
def parse(parser, log, xml):
    """ Parses Doxygen CompoundType

    :return: API dictionary
    """

    # Each "compound" has it's own XML file - read it and extract
    # the "compunddef" tags
    compound_filename = xml.attrib['refid'] + '.xml'
    compound_path = os.path.join(
        parser.doxygen_path, compound_filename)

    compound_xml = lxml.etree.parse(source=compound_path)

    api = {}

    # There can be multiple "compunddef" tags in each XML file
    # according to Doxygen's generated compound.xsd file
    for compounddef in compound_xml.findall('compounddef'):

        compunddef_api = parser.parse_element(xml=compounddef)
        api.update(compunddef_api)

    return api


@DoxygenParser.register(tag='sectiondef', attrib={'kind': 'enum'})
@DoxygenParser.register(tag='sectiondef', attrib={'kind': 'func'})
@DoxygenParser.register(tag='sectiondef', attrib={'kind': 'define'})
def parse(parser, xml):
    """ Parses Doxygen sectiondefType """

    api = {}

    for memberdef in xml.findall('memberdef'):
        api.update(parser.parse_element(xml=memberdef))

    return api


@DoxygenParser.register(tag='compounddef')
def parse(log, xml):
    """ Parses Doxygen compounddefType of kind unknown

    :return: API dictionary
    """
    log.debug("No parser for %s attrib %s", xml.tag, xml.attrib)

    return {}


@DoxygenParser.register(tag='compounddef', attrib={'kind': 'file'})
def parse(parser, xml, location_mapper):
    """ Parses Doxygen compounddefType of kind 'file'

    :return: API dictionary
    """

    full_path = xml.find("location").attrib["file"]
    relative_path = location_mapper.to_path(path=full_path)

    result = {}
    result["kind"] = "file"
    result["name"] = xml.findtext('compoundname')
    result["path"] = relative_path

    # Doxygen assigned an id to the different entities it parse including
    # files. However, when it creates links it seems it appends _source to
    # the id. So we add two mappings for the files
    refid = xml.attrib["id"]

    # Save mapping from doxygen id to unique name - we use the relative path
    # from the project dir as unique name
    parser.id_mapping[refid] = relative_path
    parser.id_mapping[refid + '_source'] = relative_path

    api = {}
    api[relative_path] = result

    #  We also parse free functions found in sectiondef tags
    for sectiondef in xml.findall('sectiondef'):
        api.update(parser.parse_element(xml=sectiondef))

    return api


@DoxygenParser.register(tag='compounddef', attrib={'kind': 'namespace'})
def parse(parser, xml):
    """ Parses Doxygen compounddefType of kind 'namespace'

    :return: API dictionary
    """

    # The output from Doxygen will have have the full scope
    # qualifier i.g. namespace etc.
    scoped_name = xml.findtext('compoundname')

    # https://docs.python.org/3/library/stdtypes.html#str.rpartition
    scope, _, name = scoped_name.rpartition('::')

    result = {}

    result["kind"] = "namespace"
    result["name"] = name
    result["scope"] = scope if scope else None
    result['briefdescription'] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result['detaileddescription'] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result['members'] = []

    # Infomration about whether a namespace is 'inline' is not yet supported
    # by doxygen:
    #   https://github.com/doxygen/doxygen/issues/6741
    result['inline'] = False

    for member in xml.findall('.//innerclass'):
        refid = member.attrib["refid"]
        result["members"].append(refid)

    for member in xml.findall('.//innernamespace'):
        refid = member.attrib["refid"]
        result["members"].append(refid)

    # In this tag we find
    #  - free functions in sectiondef tags
    api = {}

    with parser.set_scope(scoped_name):

        for sectiondef in xml.findall('sectiondef'):
            sectiondef_api = parser.parse_element(xml=sectiondef)
            result["members"] += sectiondef_api.keys()
            api.update(sectiondef_api)

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = scoped_name

    # Sort the members list such that they always appear in
    # the same order
    result["members"].sort()

    api[scoped_name] = result
    return api


@DoxygenParser.register(tag='compounddef', attrib={'kind': 'struct'})
@DoxygenParser.register(tag='compounddef', attrib={'kind': 'class'})
def parse(parser, xml):
    """ Parses Doxygen compounddefType of kind 'class'

    :return: API dictionary
    """

    api = {}

    # The output from Doxygen will have have the full scope
    # qualifier i.g. namespace etc.
    scoped_name = xml.findtext('compoundname')

    # https://docs.python.org/3/library/stdtypes.html#str.rpartition
    scope, _, name = scoped_name.rpartition('::')

    # Build the result
    result = {}

    result["kind"] = xml.attrib['kind']
    result["name"] = name
    location, body = parser.parse_element(xml=xml.find('location'))
    result["location"] = location
    result["scope"] = scope if scope else None
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["members"] = []
    result["access"] = xml.attrib["prot"]

    # Parse template arguments
    template_parameters = parse_template_parameters(xml=xml, parser=parser)

    if template_parameters is not None:
        result["template_parameters"] = template_parameters

    # Inner classes have their own tag
    for innerclass in xml.findall('.//innerclass'):
        refid = innerclass.attrib["refid"]
        result["members"].append(refid)

    api = {}

    # Create the unique name
    unique_name = scoped_name

    # Remove all whitespace - this is also done in standardes. See the README
    # on the problems of unique-name
    unique_name = unique_name.replace(" ", "")

    with parser.set_scope(unique_name):

        for member in xml.findall('.//memberdef'):
            member_api = parser.parse_element(xml=member)
            api.update(member_api)

            result['members'] += member_api.keys()

    # Sort the members list such that they always appear in
    # the same order
    result["members"].sort()

    api[unique_name] = result

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = unique_name

    return api


@DoxygenParser.register(tag='sectiondef')
@DoxygenParser.register(tag='memberdef')
def parse(log, xml):
    """ Parses Doxygen memberdefType and sectiondefType of
    kind unknown

    :return: API dictionary
    """
    log.debug("No parser for %s attrib %s", xml.tag, xml.attrib)

    return {}


@DoxygenParser.register(tag="memberdef", attrib={"kind": "enum"})
def parse(xml, parser, log, scope):
    """ Parses Doxygen memberdefType

    :return: API dictionary
    """
    result = {}
    result["kind"] = "enum"
    result["scope"] = scope
    location, body = parser.parse_element(xml=xml.find('location'))
    result['location'] = location
    result["name"] = xml.findtext("name")
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["access"] = xml.attrib["prot"]

    # Lets get all the values of the num
    values = []
    for enumvalue in xml.findall('enumvalue'):

        value = {}

        value['name'] = enumvalue.findtext('name')
        value["briefdescription"] = parser.parse_element(
            xml=enumvalue.find("briefdescription"))
        value["detaileddescription"] = parser.parse_element(
            xml=enumvalue.find("detaileddescription"))
        v = enumvalue.findtext("initializer", default="")
        if v.startswith('= '):
            v = v[2:]

        if v:
            value["value"] = v

        values.append(value)

    result["values"] = values

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = unique_name

    return {unique_name: result}


@DoxygenParser.register(tag="memberdef", attrib={"kind": "typedef"})
def parse(xml, parser, log, scope):
    """ Parses Doxygen memberdefType

    :return: API dictionary
    """
    result = {}

    definition = xml.findtext("definition")

    if definition.startswith("using"):
        result["kind"] = "using"
    elif definition.startswith("typedef"):
        result["kind"] = "typedef"
    else:
        raise RuntimeError("Unknown definition '{}'".format(definition))

    result["scope"] = scope
    location, body = parser.parse_element(xml=xml.find('location'))
    result['location'] = location
    result["name"] = xml.findtext("name")
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["access"] = xml.attrib["prot"]
    result["type"] = parser.parse_element(xml=xml.find('type'))

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = unique_name

    return {unique_name: result}


def parse_macro_parameters(xml, parser):
    """ Helper for parsing macro parameters

    :param xml: A doxygen memberdef element which may be a template
    :return: A template_parameters list or None (an empty list indicates a
        template specilization)
    """
    parameters = xml.find('parameterlist')

    if parameters is None:
        # We did not find a parameterlist element so this macro does not take
        # any elements
        return None

    # The parser for the parameterlist XML element returns a dict which has
    # parameter name as key and the description as the corresponding value
    parameters = parser.parse_element(xml=parameters)

    result = []

    for name, description in parameters:
        parameter = {'name': name}
        if description:
            parameter['description'] = description

        result.append(parameter)

    return result


@DoxygenParser.register(tag="memberdef", attrib={"kind": "define"})
def parse(xml, parser, log, scope, location_mapper):
    """ Parses Doxygen memberdefType

    :return: API dictionary
    """
    result = {}

    result["kind"] = "define"
    name = xml.findtext("name")
    result["name"] = name
    location, body = parser.parse_element(xml=xml.find('location'))

    # Doxygen seems to be reporting the wrong location information for
    # defines. I.e. the location is where the define was included - but the
    # body information seems correct so lets use that.
    #
    # Unfortunately we loose the include information here - but we may
    # fix that sometime in the future
    location = {'path': body['path'], 'line': body['line-start']}

    include_path = location_mapper.to_include(body['path'])
    if include_path:
        location['include'] = include_path

    result['location'] = location
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))

    initializer = xml.findtext("initializer", default=None)
    if initializer:
        result['initializer'] = initializer

    # Description of the tempalte parameters are in the parameterlist tags
    # with the attribute kind="param"
    parameterlists = xml.findall(
        './/parameterlist[@kind = "param"]')

    parameters = []

    for parameterlist in parameterlists:

        parameterlist = parser.parse_element(xml=parameterlist)

        log.debug("pameterlist {}".format(parameterlist))

        for name in parameterlist:

            parameter = {'name': name}

            if parameterlist[name]:
                parameter['description'] = parameterlist[name]

            parameters.append(parameter)

    if parameters:
        result['parameters'] = parameters

    log.debug("parse macro: {}".format(result))

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = result['name']

    return {result['name']: result}


@DoxygenParser.register(tag="location")
def parse(xml, parser, location_mapper):
    """ Parses Doxygen location
    :return: Location dict
    """

    # Doxygen can report two locations:
    #
    # 1. The "file" attribute which seems to be where stuff was defined
    # 2. The "bodyfile" attribute which seems to be where the body exists
    #
    # E.g. the "file" is the .h file and the "bodyfile" is the .cpp. However
    # for some things like classes the "file" and "bodyfile" are the same.
    #
    # It can also be a function that is first declared and then later
    # defined.
    #
    # In some cases we've found that the "file" and "bodyfile" point to the
    # same entity. But the "line" and "bodystart" are not equal, sometimes
    # one starts 1 line before or after the other. Which is correct actaully
    # changes. So sometimes "line" is correct and sometimes "bodyline".
    #
    # So we cannot really fix Doxygen here - we just need to live with the
    # line numbers sometimes being one off.

    # First get the location info
    location_path = location_mapper.to_path(path=xml.attrib["file"])
    location_line = int(xml.attrib["line"])
    location_include = location_mapper.to_include(path=xml.attrib["file"])

    location = {}
    location['path'] = location_path
    location['line'] = location_line

    if location_include:
        # The file was found in the inlude_paths specified
        # for the project
        location['include'] = location_include

    # Lets find the body if it exists
    body_file = xml.attrib.get('bodyfile', default=None)

    if not body_file:
        return location, None

    body_path = location_mapper.to_path(path=body_file)
    body_start = int(xml.attrib["bodystart"])
    body_end = int(xml.attrib["bodyend"])

    body = {}
    body['path'] = body_path
    body['line-start'] = body_start
    if body_end > body_start:
        body['line-end'] = body_end

    return location, body


@DoxygenParser.register(tag="parameterlist")
def parse(xml, parser):
    """ Parses Doxygen parameterlist
    :return: dictonary mapping parameter name to description
    """
    result = {}

    # The description of each parameter is stored
    # in parameteritem tags
    #
    # The strange looking .// is a ElementPath expression:
    # http://effbot.org/zone/element-xpath.htm

    for item in xml.findall('parameteritem'):

        name = item.find("parameternamelist/parametername").text

        result[name] = parser.parse_element(
            xml=item.find("parameterdescription"))

    return result


@DoxygenParser.register(tag="templateparamlist")
def parse(xml, parser):
    """ Parses Doxygen templateparamlist
    :return: List of template parameters
    """
    # Get the name and type of the parameters
    parameters = []
    for param in xml.findall('param'):

        parameter = {}

        # Look if we have a declname - sometimes Doxygen has it. It's the
        # name of the template parameter e.g. in "class T" then "T" would be
        # the declname
        template_name = param.findtext("declname", default="")
        template_type = param.findtext("type")

        # If we did not find a name it is in the type like "class T"
        if not template_name:
            template_type, template_name = template_type.split()

        parameter["type"] = [{"value": template_type}]
        parameter["name"] = template_name

        # Parse the default value
        template_default = param.find("defval")

        if template_default is not None:
            parameter["default"] = parser.parse_element(xml=template_default)

        parameters.append(parameter)

    return parameters


@DoxygenParser.register(tag="type")
@DoxygenParser.register(tag="defval")
def parse(xml, parser, log):
    """ Parses Doxygen type and defval

    :return: Type list
    """

    result = []

    def append_text(content):
        if not content or content.isspace():
            return
        else:
            result.append(
                {"value": content.strip('\r\n')})

    append_text(xml.text)

    for child in xml.getchildren():

        if match(xml=child, tag="ref"):

            link = {"url": False, "value": child.attrib["refid"]}

            result.append({"value": child.text.strip(), "link": link})

        append_text(child.tail)

    append_text(xml.tail)

    return result


def parse_template_parameters(xml, parser):
    """ Helper for parsing templates of functions, structs and classes

    :param xml: A doxygen memberdef element which may be a template
    :return: A template_parameters list or None (an empty list indicates a
        template specilization)
    """
    templatelist = xml.find('templateparamlist')

    if templatelist is None:
        # We did not find a templateparamlist element so this is not a template
        return None

    template_parameters = parser.parse_element(xml=templatelist)

    # Description of the tempalte parameters are in the parameterlist tags
    # with the attribute kind="templateparam"
    parameterlists = xml.findall(
        './/parameterlist[@kind = "templateparam"]')

    for parameterlist in parameterlists:

        parameterlist = parser.parse_element(xml=parameterlist)

        for parameter in template_parameters:

            name = parameter['name']

            if name in parameterlist:
                parameter['description'] = parameterlist[name]

    return template_parameters


@DoxygenParser.register(tag="memberdef", attrib={"kind": "function"})
def parse(xml, parser, log, scope):
    """ Parses Doxygen memberdefType

    :return: API dictionary
    """

    result = {}
    result["kind"] = "function"
    result["scope"] = scope

    location, body = parser.parse_element(xml=xml.find('location'))

    result['location'] = location
    result["name"] = xml.findtext("name")

    # Get the name and type of the parameters
    parameters = []
    for param in xml.findall('param'):

        parameter = {}
        parameter["type"] = parser.parse_element(xml=param.find("type"))

        name = param.findtext('declname')

        if name:
            parameter['name'] = name

            # If we get a name from Doxygen we need to put a space between
            # the type and the actual name
            parameter['type'].append({'value': ' ' + name})

        array = param.findtext('array')

        if array:
            # The parameter is an array
            parameter['type'][-1]['value'] += array

        # Parse the default value
        default = param.find("defval")

        if default is not None:
            parameter["type"].append({'value': ' = '})
            parameter["type"].extend(parser.parse_element(xml=default))

        parameters.append(parameter)

    # The description of the parameter is in the
    # detaileddescription section
    detaileddescription = xml.find("detaileddescription")

    # Description of the parameters are in the parameterlist tags with the
    # attribute kind="param"
    parameterlists = detaileddescription.findall(
        './/parameterlist[@kind = "param"]')

    for parameterlist in parameterlists:
        parameterlist = parser.parse_element(xml=parameterlist)

        for parameter in parameters:

            if 'name' not in parameter:
                continue

            name = parameter['name']

            if name in parameterlist:
                parameter['description'] = parameterlist[name]

    # Parse template arguments
    template_parameters = parse_template_parameters(xml=xml, parser=parser)

    if template_parameters is not None:
        result["template_parameters"] = template_parameters

    # Description of the return type
    return_type = parser.parse_element(xml=xml.find("type"))

    result["trailing_return"] = False
    if return_type:

        if return_type[0]['value'] == "auto":
            argsstring = xml.find("argsstring").text.split('->')
            if len(argsstring) == 2:
                result["trailing_return"] = True
                return_type[0]['value'] = argsstring[1].strip()

        # If we have a return type we might also have a description of it
        return_xml = detaileddescription.find(
            './/simplesect[@kind = "return"]')

        if return_xml is not None:
            return_description = parser.parse_element(xml=return_xml)
        else:
            return_description = []

        # Create the return value dictionary
        return_info = {}
        return_info["type"] = return_type
        return_info["description"] = return_description
        result["return"] = return_info

    result["is_const"] = xml.attrib["const"] == "yes"
    result["is_static"] = xml.attrib["static"] == "yes"
    result["is_explicit"] = xml.attrib["explicit"] == "yes"
    result["is_inline"] = xml.attrib["inline"] == "yes"
    result["is_virtual"] = xml.attrib["virt"] == "virtual"
    result["access"] = xml.attrib["prot"]
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["parameters"] = parameters

    # If we do not have a return type the function is either a constructor
    # or a destructor
    if "return" not in result:
        result["is_constructor"] = not result["name"].startswith("~")
        result["is_destructor"] = result["name"].startswith("~")
    else:
        result["is_constructor"] = False
        result["is_destructor"] = False

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    if "template_parameters" in result:
        unique_name += '<'
        types = []
        for parameter in result["template_parameters"]:
            for value in parameter['type']:
                types.append(value['value'])
        unique_name += ','.join(types)
        unique_name += '>'

    unique_name += '('
    parameters = []
    for parameter in result["parameters"]:
        values = []
        for value in parameter['type']:
            values.append(value['value'])
        parameters.append(''.join(values))

    unique_name += ','.join(parameters)
    unique_name += ')'

    if result["is_const"]:
        unique_name += 'const'

    # Remove all whitespace - this is also done in standardes. See the README
    # on the problems of unique-name
    unique_name = unique_name.replace(" ", "")

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = unique_name

    return {unique_name: result}


def parse_variable_type(variable_type):
    """ Parses the variable type list
    :return: (variable name, is const, is constexpr)
    """

    # To update these variables from the nested function. See:
    # https://stackoverflow.com/a/27004558/1717320
    vars = {'is_const': False, 'is_constexpr': False}

    def prune(item):

        # This prune tries to extract const and constexpr specifiers.
        tokens = item["value"].split(" ")

        if "constexpr" in tokens:
            tokens.remove("constexpr")
            vars['is_constexpr'] = True

        if "const" in tokens:
            tokens.remove("const")
            vars["is_const"] = True

        tokens = " ".join(tokens)

        # Trim multpile leading and trailing whitespace - but preseve a single
        # one if present
        item["value"] = re.sub(" +", " ", tokens)

        if item["value"]:
            return item
        else:
            return None

    variable_type = [item for item in variable_type if prune(item)]

    return variable_type, vars['is_const'], vars['is_constexpr']


@DoxygenParser.register(tag="memberdef", attrib={"kind": "variable"})
def parse(xml, parser, log, scope):
    """ Parses Doxygen variable
    :return: API dictionary
    """
    result = {}
    result["kind"] = "variable"
    result["scope"] = scope

    location, body = parser.parse_element(xml=xml.find('location'))

    result['location'] = location
    result["name"] = xml.findtext("name")
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["access"] = xml.attrib["prot"]

    # Lets get the value
    initializer_element = xml.find("initializer")
    if initializer_element is not None:

        value = initializer_element.xpath("string()")

        if value.startswith('= '):
            value = value[2:]

        result["value"] = value

    variable_type = parser.parse_element(xml=xml.find("type"))

    # Extract const and constexpr info from the variable type
    result["type"], const, constexpr = parse_variable_type(
        variable_type)

    result['is_const'] = const
    result['is_constexpr'] = constexpr
    result["is_static"] = xml.attrib["static"] == "yes"
    result["is_mutable"] = xml.attrib.get("mutable", default="no") == "yes"
    result["is_volatile"] = xml.attrib.get("volatile", default="no") == "yes"

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    return {unique_name: result}


@DoxygenParser.register(tag='simplesect', attrib={'kind': 'return'})
@DoxygenParser.register(tag="parameterdescription")
@DoxygenParser.register(tag="detaileddescription")
@DoxygenParser.register(tag="briefdescription")
def parse(xml, log, parser):
    """ Parses Doxygen descriptionType and docSimpleSectType

    :return: List of "Text information" paragraphs
    """

    paragraphs = []

    for child in xml.getchildren():

        if child.tag == 'para':
            paragraph = parser.parse_element(xml=child)
            # skip empty
            if paragraph:
                paragraphs.append(paragraph)

        else:
            log.debug("Not parsing %s", child.tag)

    return paragraphs


@DoxygenParser.register(tag='computeroutput')
@DoxygenParser.register(tag='verbatim')
def parse(parser, log, xml):
    """ Parses Doxygen code tags

    :return: List of "Text information" paragraphs
    """

    if xml.text is None:
        # This can happen if we see a verbatim element that is also a link
        # in this case Doxygen will wrap in both. Instead we will try to
        # parse the nested tag
        paragraphs = []
        for child in xml.getchildren():
            paragraphs += parser.parse_element(xml=child)

        return paragraphs

    code = xml.text.rstrip(' ')

    return [{"kind": "code", "content": code, "is_block": "\n" in code}]


@DoxygenParser.register(tag='ref')
def parse(log, xml):
    """ Parses Doxygen ref tag

    :return: List of "Text information" paragraphs
    """
    link = {"url": False, "value": xml.attrib["refid"]}
    return [{"kind": "text", "content": xml.text, "link": link}]


@DoxygenParser.register(tag='ulink')
def parse(log, xml):
    """ Parses Doxygen ulink tag

    :return: List of "Text information" paragraphs
    """
    value = xml.attrib["url"]
    if value[-1] in ',.!?:;':
        return [{"kind": "text", "content": xml.text[:-1],
                 "link": {"url": True, "value": value[:-1]}},
                {"kind": "text", "content": xml.text[-1]}]
    else:
        return [{"kind": "text", "content": xml.text,
                 "link": {"url": True, "value": value}}]


@DoxygenParser.register(tag='listitem')
@DoxygenParser.register(tag='simplesect', attrib={'kind': 'see'})
def parse(parser, log, xml):
    """ Parses Doxygen verbatim tag

    :return: List of "Text information" paragraphs
    """
    paragraphs = []
    for child in xml.getchildren():
        paragraphs.append(parser.parse_element(xml=child))

    return paragraphs


@DoxygenParser.register(tag='itemizedlist')
@DoxygenParser.register(tag='orderedlist')
def parse(parser, log, xml):
    """ Parses Doxygen ref tag

    :return: List of "Text information" paragraphs
    """

    paragraphs = []

    for item in xml.findall('listitem'):
        item_paragraphs = parser.parse_element(xml=item)
        paragraphs.append(item_paragraphs)

    return [{"kind": "list", "ordered": xml.tag == "orderedlist", "items": paragraphs}]


@DoxygenParser.register(tag='para')
def parse(parser, log, xml):
    """ Parses Doxygen docParaType

    :return: List of "Text information" paragraphs
    """

    paragraphs = []

    def append_text(content):
        if not content or content.isspace():
            return
        else:
            paragraphs.append(
                {"kind": "text", "content": content.strip()})

    append_text(xml.text)

    for child in xml.getchildren():

        if match(xml=child, tag="verbatim"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="computeroutput"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="ref"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="ulink"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="orderedlist"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="itemizedlist"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="simplesect", attrib={"kind": "see"}):
            paragraphs += parser.parse_element(xml=child)

        else:
            log.debug("For %s not parsing %s attrib %s",
                      xml.tag, child.tag, child.attrib)

        append_text(child.tail)

    append_text(xml.tail)

    return paragraphs
