import pyquery
import lxml
import mock
import logging

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


def parse_paragraphs(parser, xml):
    """ Parses Doxygen docParaType

    XML Schema:
        <xsd:complexType name="docParaType" mixed="true">
        <xsd:group ref="docCmdGroup" minOccurs="0" maxOccurs="unbounded" />
        </xsd:complexType>

    XML Schema:

        <xsd:group name="docCmdGroup">
        <xsd:choice>
        <xsd:group ref="docTitleCmdGroup"/>
        <xsd:element name="linebreak" type="docEmptyType" />
        <xsd:element name="hruler" type="docEmptyType" />
        <xsd:element name="preformatted" type="docMarkupType" />
        <xsd:element name="programlisting" type="listingType" />
        <xsd:element name="verbatim" type="xsd:string" />
        <xsd:element name="indexentry" type="docIndexEntryType" />
        <xsd:element name="orderedlist" type="docListType" />
        <xsd:element name="itemizedlist" type="docListType" />
        <xsd:element name="simplesect" type="docSimpleSectType" />
        <xsd:element name="title" type="docTitleType" />
        <xsd:element name="variablelist" type="docVariableListType" />
        <xsd:element name="table" type="docTableType" />
        <xsd:element name="heading" type="docHeadingType" />
        <xsd:element name="image" type="docImageType" />
        <xsd:element name="dotfile" type="docFileType" />
        <xsd:element name="mscfile" type="docFileType" />
        <xsd:element name="diafile" type="docFileType" />
        <xsd:element name="toclist" type="docTocListType" />
        <xsd:element name="language" type="docLanguageType" />
        <xsd:element name="parameterlist" type="docParamListType" />
        <xsd:element name="xrefsect" type="docXRefSectType" />
        <xsd:element name="copydoc" type="docCopyType" />
        <xsd:element name="blockquote" type="docBlockQuoteType" />
        <xsd:element name="parblock" type="docParBlockType" />
        </xsd:choice>
    </xsd:group>

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
            parser.log.debug("Not parsing %s", child.tag)

        append_text(child.tail)

    append_text(xml.tail)

    return paragraphs


def parse_descriptiontype(parser, xml):
    """ Parses Doxygen descriptionType

    XML Schema:

        <xsd:complexType name="descriptionType" mixed="true">
        <xsd:sequence>
        <xsd:element name="title" type="xsd:string" minOccurs="0"/>
        <xsd:element name="para" type="docParaType" minOccurs="0" maxOccurs="unbounded" />
        <xsd:element name="sect1" type="docSect1Type" minOccurs="0" maxOccurs="unbounded" />
        <xsd:element name="internal" type="docInternalType" minOccurs="0" />
        </xsd:sequence>
        </xsd:complexType>
    """

    paragraphs = []

    for child in xml.getchildren():

        if child.tag == 'para':
            paragraphs += parse_paragraphs(parser=parser, xml=child)

        else:
            parser.log.debug("Not parsing %s", child.tag)

    return paragraphs


def parse_function_parameters(parser, xml):
    """ Parse the parameters of a function.

    XML Schema:

    <xsd:complexType name="memberdefType">
        <xsd:sequence>
            ...
            <xsd:element name="param" type="paramType" minOccurs="0" maxOccurs="unbounded" />
            ...
            <xsd:element name="detaileddescription" type="descriptionType" minOccurs="0" />
            ...
        </xsd:sequence>
        <xsd:attribute name="kind" type="DoxMemberKind" />
        ...
    </xsd:complexType>

    """
    assert xml.tag == 'memberdef'
    assert xml.attrib['kind'] == 'function'

    parameters = []

    # First we get the name and type of the parameters

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

                parameter['description'] = parse_descriptiontype(
                    parser=parser, xml=description)

                break

    return parameters


def _test_pyquery_text():

    pq = pyquery.PyQuery(xml, parser='xml')

    # pq.tag

    for node in pq:
        print("tag = %s" % node.tag)

        for child in node.getchildren():
            node.remove(child)

    print(unicode(pq))

    # print(pq.text())

    assert 0


def test_lxml(caplog):

    caplog.set_level(logging.DEBUG)

    root = lxml.etree.fromstring(xml)

    parser = mock.Mock()
    parser.log = logging.getLogger("test")

    result = {}

    result["type"] = "function"
    result["name"] = root.find("name").text
    result["return_type"] = root.find("type").text
    result["is_const"] = root.attrib["const"] == "yes"
    result["is_static"] = root.attrib["const"] == "yes"
    result["access"] = root.attrib["prot"]
    result["briefdescription"] = parse_descriptiontype(
        parser=parser, xml=root.find("briefdescription"))
    result["detaileddescription"] = parse_descriptiontype(
        parser=parser, xml=root.find("detaileddescription"))
    result["parameters"] = parse_function_parameters(
        parser=parser, xml=root)

    print(result)

    assert 0
