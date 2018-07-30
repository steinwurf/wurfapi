import glob
import os
import pyquery
import lxml
import inspect
import contextlib
import copy


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

    def __init__(self, doxygen_path, project_path, log):
        """ Create a new DoxygenParser

        :param doxygen_path: The path to where the Doxygen XML is
            located.
        :param project_path: The path to the project as a String. The path is
            important as we use it to compute the relative paths to the files
            indexed by Doxygen. So e.g. if we want to generate links to GitHub
            etc. we need the relative path to the files with root of the
            project.
        :param log: Log object
        """
        self.doxygen_path = doxygen_path
        self.project_path = project_path
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

        return replace_with(replace=self.id_mapping, data=api)

    def parse_element(self, xml):
        """ Parse an XML element """

        parser = self._find_in_list(xml=xml)

        # Inject needed arguments
        args = {'xml': xml}

        require_arguments = inspect.getargspec(parser.function)[0]

        for argument in require_arguments:
            if argument == "parser":
                args["parser"] = self
            elif argument == "log":
                args["log"] = self.log
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

    def relative_path(self, path):
        """ Return the relative path from the project_path """
        path = os.path.relpath(path=path, start=self.project_path)

        # Make sure we use unix / linux style paths - also on windows
        path = path.replace('\\', '/')

        return path

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
def parse(parser, xml):
    """ Parses Doxygen sectiondefType of kind 'func' """

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
def parse(parser, xml):
    """ Parses Doxygen compounddefType of kind 'file'

    :return: API dictionary
    """

    # In this tag we find
    #  - free functions in sectiondef tags
    api = {}

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

    result["type"] = "namespace"
    result["name"] = name
    result["scope"] = scope
    result['briefdescription'] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result['detaileddescription'] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result['members'] = []

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
    result = {
        'type': xml.attrib['kind'],
        'name': name,
        'location': parser.parse_element(xml=xml.find('location')),
        'scope': scope,
        'briefdescription': parser.parse_element(
            xml=xml.find("briefdescription")),
        'detaileddescription': parser.parse_element(
            xml=xml.find("detaileddescription")),
        'members': []
    }

    api = {}

    with parser.set_scope(scoped_name):

        for member in xml.findall('.//memberdef'):
            member_api = parser.parse_element(xml=member)
            api.update(member_api)

            result['members'] += member_api.keys()

    # Sort the members list such that they always appear in
    # the same order
    result["members"].sort()

    api[scoped_name] = result

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = scoped_name

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
    result["type"] = "enum"
    result["scope"] = scope
    result['location'] = parser.parse_element(xml=xml.find('location'))
    result["name"] = xml.findtext("name")
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))

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
        value["value"] = v

        values.append(value)

    result["values"] = values

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    return {unique_name: result}


@DoxygenParser.register(tag="location")
def parse(xml, parser):
    """ Parses Doxygen memberdefType

    :return: Location dict
    """
    result = {}
    file_path = xml.attrib["file"]
    result['file'] = parser.relative_path(path=file_path)

    result['line-start'] = int(xml.attrib["bodystart"])
    result['line-stop'] = int(xml.attrib["bodyend"])

    return result


@DoxygenParser.register(tag="memberdef", attrib={"kind": "function"})
def parse(xml, parser, log, scope):
    """ Parses Doxygen memberdefType

    :return: API dictionary
    """

    result = {}

    # First we get the name and type of the parameters
    parameters = []
    for param in xml.findall('param'):

        assert param.tag == 'param'

        parameter = {}

        parameter['type'] = param.findtext('type')
        parameter['name'] = param.findtext('declname')
        parameter['description'] = ''

        parameters.append(parameter)

    # The description of the parameter is in the
    # detaileddescription section

    detaileddescription = xml.find("detaileddescription")

    # The description of each parameter is stored
    # in parameteritem tags
    #
    # The strange looking .// is a ElementPath expression:
    # http://effbot.org/zone/element-xpath.htm

    for item in detaileddescription.findall('.//parameteritem'):

        name = item.find("parameternamelist/parametername").text

        for parameter in parameters:

            if name == parameter['name']:

                description = item.find("parameterdescription")

                parameter['description'] = parser.parse_element(
                    xml=description)

                break

    # Description of the return type
    return_xml = detaileddescription.find('.//simplesect[@kind = "return"]')

    if return_xml is not None:
        return_description = parser.parse_element(xml=return_xml)
    else:
        return_description = []

    result["type"] = "function"
    result["scope"] = scope
    result["name"] = xml.findtext("name")
    result["return_type"] = xml.findtext("type")
    result["signature"] = result["name"] + xml.findtext("argsstring")
    result["return_description"] = return_description
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

    # Construct the unique name
    unique_name = scope + '::' + result["name"] if scope else result["name"]

    unique_name += '('
    types = [parameter['type'] for parameter in parameters]
    unique_name += ','.join(types)
    unique_name += ')'

    if result["is_const"]:
        unique_name += 'const'

    # Remove all whitespace - this is also done in standardes. See the README
    # on the problems of unique-name
    unique_name = unique_name.replace(" ", "")

    # Save mapping from doxygen id to unique name
    parser.id_mapping[xml.attrib["id"]] = unique_name

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
            paragraphs += parser.parse_element(xml=child)

        else:
            log.debug("Not parsing %s", child.tag)

    return paragraphs


@DoxygenParser.register(tag='computeroutput')
@DoxygenParser.register(tag='verbatim')
def parse(log, xml):
    """ Parses Doxygen code tags

    :return: List of "Text information" paragraphs
    """

    # code = xml.text.strip()
    code = xml.text.rstrip(' ')

    return [{"type": "code", "content": code, "is_block": "\n" in code}]


@DoxygenParser.register(tag='ref')
def parse(log, xml):
    """ Parses Doxygen ref tag

    :return: List of "Text information" paragraphs
    """
    link = xml.attrib["refid"]
    return [{"type": "text", "content": xml.text, "link": link}]


@DoxygenParser.register(tag='simplesect', attrib={'kind': 'see'})
def parse(parser, log, xml):
    """ Parses Doxygen verbatim tag

    :return: List of "Text information" paragraphs
    """
    paragraphs = []
    for child in xml.getchildren():
        paragraphs += parser.parse_element(xml=child)

    return paragraphs


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
                {"type": "text", "content": content.strip()})

    append_text(xml.text)

    for child in xml.getchildren():

        if match(xml=child, tag="verbatim"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="computeroutput"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="ref"):
            paragraphs += parser.parse_element(xml=child)

        elif match(xml=child, tag="simplesect", attrib={"kind": "see"}):
            paragraphs += parser.parse_element(xml=child)

        else:
            log.debug("For %s not parsing %s attrib %s",
                      xml.tag, child.tag, child.attrib)

        append_text(child.tail)

    append_text(xml.tail)

    return paragraphs
