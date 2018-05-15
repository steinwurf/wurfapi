import glob
import os
import pyquery


def parse_text(parser, xml):
    # Sanity checks
    assert parser.element_type(xml=xml) in [
        'briefdescription', 'detaileddescription']

    return xml.text()


def parse_function(parser, xml, scope=None):
    """ Parses a function

    :param parser: A DoxygenParser instance
    :param xml: pyquery.PyQuery object representing the function
    :param scope: The enclosing scope as a string or None if the
        function is not enclosed in a scope.
    :return: The API where there function type will be stored
    """
    # Sanity checks
    assert parser.element_type(xml=xml) == 'memberdef'
    assert xml.attr('kind') == 'function'

    # The name of the function
    name = xml('name').text()

    # Extract the parameters
    parameters = []

    for param in xml.items('param'):
        parameter = {
            # Trim off all newlines: https://stackoverflow.com/a/37001613/1717320
            'type': " ".join(param('type').text().split()),
            'name': " ".join(param('declname').text().split())
        }

        parameters.append(parameter)

    # Construct the unique name
    unique_name = scope + '::' + name if scope else name

    unique_name += '('
    types = [parameter['type'] for parameter in parameters]
    unique_name += ','.join(types)
    unique_name += ')'

    if xml.attr('const') == "yes":
        unique_name += 'const'

    # Remove all whitespace - this is also done in standardes. See the README
    # on the problems of unique-name
    unique_name = unique_name.replace(" ", "")

    # Get the location
    file_path = xml('location').attr("file")
    file_path = parser.relative_path(path=file_path)

    file_line_start = int(xml('location').attr("line"))

    # Build the result
    result = {
        'type': 'function',
        'name': name,
        'location': {'file': file_path, 'line': file_line_start},
        'scope': scope,
        # We using the children selector of pyquery to only get
        # direct children of the "memberdef" element. There are nested
        # "type" elements in the "param" elements
        #
        # PyQuery insert newlines when there are nested "ref" elements
        # in the "type" element. We replace these with spaces
        'return_type':
            xml.children('type').text().replace('\n', ' '),
        'is_const': xml.attr('const') == "yes",
        'is_static': xml.attr('static') == "yes",
        'access': xml.attr('prot'),
        'briefdescription':
            parse_text(parser, xml.children('briefdescription')),
        'detaileddescription':
            parse_text(parser, xml.children('detaileddescription')),
        'parameters': parameters
    }

    # Store the information in the API
    api = {unique_name: result}

    return api


def parse_class_or_struct(parser, xml):
    """ Parses a class or struct

    :param parser: A DoxygenParser instance
    :param xml: pyquery.PyQuery object representing the function
    :return: The API where there class/struct and it's members will be stored
    """

    # Sanity check
    assert parser.element_type(xml=xml) == 'compounddef'
    assert xml.attr('kind') in ['class', 'struct']

    # The output from Doxygen will have have the full scope
    # qualifier i.g. namespace etc.
    scoped_name = xml('compoundname').text()

    # https://docs.python.org/3/library/stdtypes.html#str.rpartition
    scope, _, name = scoped_name.rpartition('::')

    # Get the location
    location = xml.children('location')
    file_path = location.attr("file")
    file_path = parser.relative_path(path=file_path)

    file_line_start = int(location.attr("line"))

    # Build the result
    result = {
        'type': xml.attr('kind'),
        'name': name,
        'location': {'file': file_path, 'line': file_line_start},
        'scope': scope,
        'briefdescription': xml.children('briefdescription').text(),
        'detaileddescription': xml.children('detaileddescription').text(),
        'members': []
    }

    api = {}

    for member in xml.items('memberdef'):

        if parser.supports(xml=member):

            member_api = parser.parse_element(xml=member, scope=scoped_name)
            api.update(member_api)

            result['members'] += member_api.keys()

    api[scoped_name] = result
    return api


default_parsers = {
    'parse_class': parse_class_or_struct,
    'parse_struct': parse_class_or_struct,
    'parse_function': parse_function
}


class DoxygenParser(object):

    def __init__(self, project_path, log, parsers=default_parsers):
        """ Create a new DoxygenReader

        :param project_path: The path to the project as a String. The path is
            important as we use it to compute the relative paths to the files
            indexed by Doxygen. So e.g. if we want to generate links to GitHub
            etc. we need the relative path to the files with root of the
            project.
        :param log: Log object
        :param parsers: Dictionary with the following specific layout:
            readers = {
                "read_xyz": func1,
                "read_abc": func2
                }

                The keys to the dict have the "parse_" prefix the postfix
                part is the "kind" of XML element they parse. Doxygen uses
                a "kind" attribute on the XML elements we are interested in.
                The value in the dict a Python function or callable. Which
                has the following signature f(parser, xml, **kwargs)

                The parser parameter is a DoxygenParser object, the xml
                parameter is the Doxygen XML element we are parsing. The
                **kwargs are optional keyword arguments.
        """
        self.parsers = parsers
        self.project_path = project_path
        self.log = log

    def parse_api(self, doxygen_path):
        """ Read the generated Doxygen XML

        :param doxygen_path: The path to the generated Doxygen XML as a string
        :return: An API dictionary
        """

        xml = self.xml_from_path(doxygen_path=doxygen_path)
        assert len(xml) > 0

        # The dictionary we will store the API in
        api = {}

        for element in xml:

            # Sanity check
            assert self.element_type(xml=element) == "compounddef"

            if self.supports(xml=element):

                element_api = self.parse_element(xml=element)
                assert len(element_api) > 0

                api.update(element_api)

            else:
                kind = element.attr('kind')
                self.log.warning('Not supported {}'.format(kind))

        return api

    def parse_element(self, xml, **kwargs):
        """ Parse a specific Doxygen XML element

        :param xml: A pyquery.PyQuery object representing a Doxygen XML element
        :param kwargs: Optional keyword arguments passed between the diffferent
            readers
        """
        parser = 'parse_' + xml.attr('kind')
        parser_function = self.parsers[parser]

        return parser_function(parser=self, xml=xml, **kwargs)

    def supports(self, xml):
        """ Check if we have a parser for the "kind" of element.

        The Doxygen XML tags we are interested in all have "kind=xyz" as an
        attribute. Here we check if we have a parser for the specific type.

        :param xml: The Doxygen XML as a pyquery.PyQuery object
        :return: True if we have a reader for the "kind" of element. Otherwise
            False
        """

        parser = 'parse_' + xml.attr('kind')
        return parser in self.parsers

    def element_type(self, xml):
        """ Return the XML element type. We use a bit of pyquery internals to
        do this. But we need to perform some sanity checks in the parser
        functions.

        Example: If we are parsing a memberdef element the _element_type should
        return "memberdef" when passing the pyquery.PyQuery object

        :param xml: pyquery.PyQuery element we want to know the type of
        :return: Element tag as a string
        """
        assert(xml.size() == 1)
        return xml[0].tag

    def relative_path(self, path):
        """ Return the relative path from the project_path """
        path = os.path.relpath(path=path, start=self.project_path)

        # Make sure we use unix / linux style paths - also on windows
        path = path.replace('\\', '/')

        return path

    @staticmethod
    def xml_from_path(doxygen_path):
        """ Read the generated Doxygen XML

        :param doxygen_path: The path to the generated Doxygen XML as a
            string
        :return: A list of pyquery.PyQuery objects representing the
            different "compunddef" elements.
        """
        # Find the index XML file
        index_path = os.path.join(doxygen_path, 'index.xml')

        assert(os.path.isfile(index_path))

        index_xml = pyquery.PyQuery(
            filename=index_path, parser='xml', encoding='utf-8')

        # We extract the compound definitions XML "compunddef" tag
        # These contain the information we need.
        compound_definitions = []

        # Iterate thought the "compound" elements of the Doxygen index.xml
        for compound in index_xml.items('compound'):

            # Each "compound" has it's own XML file - read it and extract the
            # "compunddef" tags
            compound_filename = compound.attr('refid') + '.xml'
            compound_path = os.path.join(doxygen_path, compound_filename)

            compound_xml = pyquery.PyQuery(
                filename=compound_path, parser='xml', encoding='utf-8')

            # There can be multiple "compunddef" tags in each XML file
            # according to Doxygen's generated compound.xsd file

            compound_definitions += compound_xml.items('compounddef')

        return compound_definitions
