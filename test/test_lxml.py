import pyquery
import lxml
import mock
import logging
import inspect
import contextlib

xml = """
<memberdef kind="function" id="classproject_1_1coffee_1_1machine_1ac4b1c2e8d19a4bfae80aa40eeaf8c7db" prot="protected" static="no" const="yes" explicit="no" inline="no" virt="non-virtual">
<type>uint32_t</type>
<definition>uint32_t project::coffee::machine::set</definition>
<argsstring>(const heat &amp;h, int max) const</argsstring>
<name>set</name>
<param>
    <type>const heat &amp;</type>
    <declname>h</declname>
</param>
<param>
    <type>int</type>
    <declname>max</declname>
</param>
<briefdescription>
    <para>Set the heat. </para>
</briefdescription>
<detaileddescription>
     <para>This function is use to set the head of the machine. <verbatim>void yes();</verbatim></para>
     <para>But maybe it also does other things?</para>
     <para>
        <parameterlist kind="param">
            <parameteritem>
                <parameternamelist>
                    <parametername>h</parametername>
                </parameternamelist>
                <parameterdescription>
                    <para>Set the heat object.</para>
                </parameterdescription>
            </parameteritem>
        </parameterlist>
        Test this break
    </para>
    <para>
        <parameterlist kind="param">
            <parameteritem>
                <parameternamelist>
                    <parametername>max</parametername>
                </parameternamelist>
                <parameterdescription>
                    <para>The maximum heat value. </para>
                </parameterdescription>
            </parameteritem>
        </parameterlist>
        <simplesect kind="return">
            <para>The current heat. <verbatim>for (uint64_t i = 0; i &lt; 3; ++i)
                {
                std::cout &lt;&lt; i &lt;&lt; &quot;\n&quot;;
                }
                </verbatim>
            </para>
        </simplesect>
        And then some text
    </para>
</detaileddescription>
<inbodydescription></inbodydescription>
<location file="/home/mvp/dev/steinwurf/wurfapi/pytest_temp/unit_tests/test_read_function0/cpp_coffee/src/coffee/coffee.h" line="47" column="1"/>
</memberdef>"""


# def parse_paragraphs(log, xml):
#     """ Parses Doxygen docParaType

#     XML Schema:
#         <xsd:complexType name="docParaType" mixed="true">
#         <xsd:group ref="docCmdGroup" minOccurs="0" maxOccurs="unbounded" />
#         </xsd:complexType>

#     XML Schema:

#         <xsd:group name="docCmdGroup">
#         <xsd:choice>
#         <xsd:group ref="docTitleCmdGroup"/>
#         <xsd:element name="linebreak" type="docEmptyType" />
#         <xsd:element name="hruler" type="docEmptyType" />
#         <xsd:element name="preformatted" type="docMarkupType" />
#         <xsd:element name="programlisting" type="listingType" />
#         <xsd:element name="verbatim" type="xsd:string" />
#         <xsd:element name="indexentry" type="docIndexEntryType" />
#         <xsd:element name="orderedlist" type="docListType" />
#         <xsd:element name="itemizedlist" type="docListType" />
#         <xsd:element name="simplesect" type="docSimpleSectType" />
#         <xsd:element name="title" type="docTitleType" />
#         <xsd:element name="variablelist" type="docVariableListType" />
#         <xsd:element name="table" type="docTableType" />
#         <xsd:element name="heading" type="docHeadingType" />
#         <xsd:element name="image" type="docImageType" />
#         <xsd:element name="dotfile" type="docFileType" />
#         <xsd:element name="mscfile" type="docFileType" />
#         <xsd:element name="diafile" type="docFileType" />
#         <xsd:element name="toclist" type="docTocListType" />
#         <xsd:element name="language" type="docLanguageType" />
#         <xsd:element name="parameterlist" type="docParamListType" />
#         <xsd:element name="xrefsect" type="docXRefSectType" />
#         <xsd:element name="copydoc" type="docCopyType" />
#         <xsd:element name="blockquote" type="docBlockQuoteType" />
#         <xsd:element name="parblock" type="docParBlockType" />
#         </xsd:choice>
#     </xsd:group>

#     """

#     paragraphs = []

#     def append_text(content):
#         if not content or content.isspace():
#             return
#         else:
#             paragraphs.append(
#                 {"type": "text", "content": content.strip()})

#     append_text(xml.text)

#     for child in xml.getchildren():

#         if child.tag == 'verbatim':
#             paragraphs.append(
#                 {"type": "code", "content": child.text})
#         else:
#             log.debug("Not parsing %s", child.tag)

#         append_text(child.tail)

#     append_text(xml.tail)

#     return paragraphs


# def parse_descriptiontype(log, xml):
#     """ Parses Doxygen descriptionType

#     XML Schema:

#         <xsd:complexType name="descriptionType" mixed="true">
#         <xsd:sequence>
#         <xsd:element name="title" type="xsd:string" minOccurs="0"/>
#         <xsd:element name="para" type="docParaType" minOccurs="0" maxOccurs="unbounded" />
#         <xsd:element name="sect1" type="docSect1Type" minOccurs="0" maxOccurs="unbounded" />
#         <xsd:element name="internal" type="docInternalType" minOccurs="0" />
#         </xsd:sequence>
#         </xsd:complexType>
#     """

#     paragraphs = []

#     for child in xml.getchildren():

#         if child.tag == 'para':
#             paragraphs += parse_paragraphs(log=log, xml=child)

#         else:
#             log.debug("Not parsing %s", child.tag)

#     return paragraphs


# def parse_function_parameters(log, xml):
#     """ Parse the parameters of a function.

#     XML Schema:

#     <xsd:complexType name="memberdefType">
#         <xsd:sequence>
#             ...
#             <xsd:element name="param" type="paramType" minOccurs="0" maxOccurs="unbounded" />
#             ...
#             <xsd:element name="detaileddescription" type="descriptionType" minOccurs="0" />
#             ...
#         </xsd:sequence>
#         <xsd:attribute name="kind" type="DoxMemberKind" />
#         ...
#     </xsd:complexType>

#     """
#     assert xml.tag == 'memberdef'
#     assert xml.attrib['kind'] == 'function'

#     parameters = []

#     # First we get the name and type of the parameters

#     for param in xml.findall('param'):

#         assert param.tag == 'param'

#         parameter = {}

#         parameter['type'] = param.findtext('type')
#         parameter['name'] = param.findtext('declname')
#         parameter['description'] = ''

#         parameters.append(parameter)

#     # The description of the parameter is in the
#     # detaileddescription section

#     detaileddescription = xml.find("detaileddescription")

#     # The description of each parameter is stored
#     # in parameteritem tags
#     #
#     # The strange looking .// is a ElementPath expression:
#     # http://effbot.org/zone/element-xpath.htm

#     for item in detaileddescription.findall('.//parameteritem'):

#         name = item.find("parameternamelist/parametername").text

#         for parameter in parameters:

#             if name == parameter['name']:

#                 description = item.find("parameterdescription")

#                 parameter['description'] = parse_descriptiontype(
#                     log=log, xml=description)

#                 break

#     return parameters


# def _test_pyquery_text():

#     pq = pyquery.PyQuery(xml, parser='xml')

#     # pq.tag

#     for node in pq:
#         print("tag = %s" % node.tag)

#         for child in node.getchildren():
#             node.remove(child)

#     print(unicode(pq))

#     # print(pq.text())

#     assert 0


# def test_lxml(caplog):

#     caplog.set_level(logging.DEBUG)

#     root = lxml.etree.fromstring(xml)

#     parser = mock.Mock()
#     parser.log = logging.getLogger("test")
#     log = parser.log

#     result = {}

#     result["type"] = "function"
#     result["name"] = root.find("name").text
#     result["return_type"] = root.find("type").text
#     result["is_const"] = root.attrib["const"] == "yes"
#     result["is_static"] = root.attrib["const"] == "yes"
#     result["access"] = root.attrib["prot"]
#     result["briefdescription"] = parse_descriptiontype(
#         log=log, xml=root.find("briefdescription"))
#     result["detaileddescription"] = parse_descriptiontype(
#         log=log, xml=root.find("detaileddescription"))
#     result["parameters"] = parse_function_parameters(
#         log=log, xml=root)

#     print(result)

# assert 0


class ParserFunction(object):

    def __init__(self, function, tag, attrib):
        self.function = function
        self.tag = tag
        self.attrib = attrib if attrib else {}

    def can_parse(self, tag, attrib):
        if tag != self.tag:
            return False

        for key in self.attrib:
            try:
                if self.attrib[key] != attrib[key]:
                    return False
            except KeyError:
                return False

        return True

    def __repr__(self):
        return ("<{} tag='{}', attrib='{}'>".format(
            self.__class__.__name__, self.tag, self.attrib))


class ParserList(object):

    # Default parsers
    default_parsers = []

    def __init__(self, project_path, log, use_default=True):
        """ Create a new DoxygenParser

        :param project_path: The path to the project as a String. The path is
            important as we use it to compute the relative paths to the files
            indexed by Doxygen. So e.g. if we want to generate links to GitHub
            etc. we need the relative path to the files with root of the
            project.
        :param log: Log object
        """
        self.log = log
        self.parsers = []

        # Scope variable used to track the C++ scope of member functions etc.
        self.scope = None

        if use_default:
            self.parsers = ParserList.default_parsers

    def add_parser(self, function, tag, attrib):

        self._add_to_list(
            parser_list=self.parsers, tag=tag, attrib=attrib,
            function=function)

    @contextlib.contextmanager
    def set_scope(self, scope):
        assert self.scope is None

        self.scope = scope
        yield
        self.scope = None

    def parse_index(self, doxygen_path):
        pass

    def parse_element(self, xml):
        """ Parse an XML element """

        parser = self._find_in_list(
            parser_list=self.parsers, tag=xml.tag, attrib=xml.attrib)

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

    def relative_path(self, path):
        """ Return the relative path from the project_path """
        path = os.path.relpath(path=path, start=self.project_path)

        # Make sure we use unix / linux style paths - also on windows
        path = path.replace('\\', '/')

        return path

    @staticmethod
    def _find_in_list(parser_list, tag, attrib):
        """ Find the parser function for a specific XML element. """

        for parser in parser_list:

            if parser.can_parse(tag=tag, attrib=attrib):
                return parser
        else:
            raise RuntimeError(
                "No parser for tag {} attrib {}\nCandidates are: {}".format(
                    tag, attrib, parser_list))

    @staticmethod
    def _add_to_list(parser_list, tag, attrib, function):
        """ Add the parser function for a specific XML element. """

        for parser in parser_list:

            if parser.can_parse(tag=tag, attrib=attrib):
                raise RuntimeError("Parser {} {} Already exists".format(
                    tag, attrib))

        else:
            # If the parser does not already exist we add it
            parser = ParserFunction(
                function=function, tag=tag, attrib=attrib)

            parser_list.append(parser)

    @staticmethod
    def register(tag, attrib=None):
        """ Decorator for registering parser functions.

        The decorator will take an XML tag and optional attributes and
        use that to register a parser function.
        """
        def _register(function):

            ParserList._add_to_list(
                parser_list=ParserList.default_parsers, tag=tag,
                attrib=attrib, function=function)

            return function

        return _register


@ParserList.register(tag="parameterdescription")
@ParserList.register(tag="detaileddescription")
@ParserList.register(tag="briefdescription")
def parse(xml, log, parser):
    """ Parses Doxygen descriptionType

    :return: List of "Text information" paragraphs
    """

    paragraphs = []

    for child in xml.getchildren():

        if child.tag == 'para':
            paragraphs += parser.parse_element(xml=child)

        else:
            log.debug("Not parsing %s", child.tag)

    return paragraphs


@ParserList.register(tag='para')
def parse(log, xml):
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

        if child.tag == 'verbatim':
            paragraphs.append(
                {"type": "code", "content": child.text})
        else:
            log.debug("Not parsing %s", child.tag)

        append_text(child.tail)

    append_text(xml.tail)

    return paragraphs


@ParserList.register(tag="memberdef", attrib={"kind": "function"})
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

    result["type"] = "function"
    result["scope"] = scope if scope else "global"
    result["name"] = xml.find("name").text
    result["return_type"] = xml.find("type").text
    result["is_const"] = xml.attrib["const"] == "yes"
    result["is_static"] = xml.attrib["const"] == "yes"
    result["access"] = xml.attrib["prot"]
    result["briefdescription"] = parser.parse_element(
        xml=xml.find("briefdescription"))
    result["detaileddescription"] = parser.parse_element(
        xml=xml.find("detaileddescription"))
    result["parameters"] = parameters

    return result


def test_element_parser(testdirectory):

    log = mock.Mock()

    ep = ParserList(project_path=testdirectory.path(), log=log)

    root = lxml.etree.fromstring(xml)

    with ep.set_scope("project"):
        result = ep.parse_element(xml=root)

    print(result)

    result = ep.parse_element(xml=root)

    print(result)
