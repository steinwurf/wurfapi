import os
import shutil

# Doxygen uses the Doxyfile as configuration file. You can read more
# about it here:
# http://www.stack.nl/~dimitri/doxygen/manual/config.html
DOXYFILE_TEMPLATE = r"""
PROJECT_NAME     = "{name}"
OUTPUT_DIRECTORY = {output_path}
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
RECURSIVE        = {recursive}
INPUT            = {source_path}
ENABLE_PREPROCESSING = YES
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
XML_OUTPUT = xml
ALIASES = "rst=\verbatim embed:rst"
ALIASES += "endrst=\endverbatim"
{extra}
""".strip()


class DoxygenGenerator(object):

    def __init__(self, doxygen_executable, runner, recursive,
                 source_path, output_path):
        self.doxygen_executable = doxygen_executable
        self.runner = runner
        self.recursive = recursive
        self.source_path = source_path
        self.output_path = output_path

        assert(os.path.isdir(self.source_path))
        assert(os.path.isdir(self.output_path))

    def generate(self):
        """ Generate the Doxygen XML.

        We do not have to remove any old XML or similar since we use the
        index.xml file to parse the rest.. So if some stale information is
        in the output folder it is ok - we will not use it anyway

        :return: The path to the generated XML
        """

        # Write Doxyfile
        doxyfile_content = DOXYFILE_TEMPLATE.format(
            name='wurfapi',
            output_path=self.output_path,
            source_path=self.source_path,
            recursive="YES" if self.recursive else "NO",
            extra="")

        doxyfile_path = os.path.join(self.output_path, 'Doxyfile')
        with open(doxyfile_path, 'w') as doxyfile:

            doxyfile.write(doxyfile_content)

        # @todo: Doxygen generates a bunch of warnings. We should
        #        propagate these somehow - if you want to know what
        #        has not been documented etc.
        self.runner.run(command=self.doxygen_executable + ' Doxyfile',
                        cwd=self.output_path)

        # The Doxygen XML is written to the 'xml' subfolder of the
        # output directory
        return os.path.join(self.output_path, 'xml')
