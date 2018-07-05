import pyquery
import lxml

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


def parse_paragraphs(xml):
    



def parse_descriptiontype(parser, xml):
    """ Parses Doxygen descriptionType

    <xsd:complexType name="descriptionType" mixed="true">
    <xsd:sequence>
      <xsd:element name="title" type="xsd:string" minOccurs="0"/>
      <xsd:element name="para" type="docParaType" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="sect1" type="docSect1Type" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="internal" type="docInternalType" minOccurs="0" />
    </xsd:sequence>
    </xsd:complexType>
    """

    for nodes in xml:
        




def test_pyquery_text():

    pq = pyquery.PyQuery(xml, parser='xml')

    # pq.tag

    for node in pq:
        print("tag = %s" % node.tag)

        for child in node.getchildren():
            node.remove(child)

    print(unicode(pq))

    # print(pq.text())

    assert 0


def _test_lxml():

    root = lxml.etree.fromstring(xml)

    def visit(node, level):
        for child in node.getchildren():
            if not child.text:
                text = "None"
            else:
                text = child.text

            if child.tail:
                text += child.tail

            print(" "*level + child.tag + " => " + text)

            visit(node=child, level=level+4)

    visit(node=root, level=0)

    assert 0
