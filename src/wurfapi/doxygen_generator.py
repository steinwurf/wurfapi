import os
import shutil
import pprint

import wurfapi.doxygen_error

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
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
XML_OUTPUT = xml
{extra}
""".strip()


class DoxygenGenerator(object):

    def __init__(self, doxygen_executable, runner, recursive,
                 source_paths, output_path, warnings_as_error):
        """ Generate the doxygen XML.

        :param doxygen_executable: Path to the Doxygen executable.
        :param runner: The subprocess run wrapper.
        :param recursive: Doxygen option
        :param source_paths: Doxygen option
        :param output_path: Doxygen option
        :param warnings_as_errors: If True we raise an error if Doxygen
            produces any warnings. If False we ignore any Doxygen
            warnings.
        """
        self.doxygen_executable = doxygen_executable
        self.runner = runner
        self.recursive = recursive
        self.source_paths = source_paths
        self.output_path = output_path
        self.warnings_as_error = warnings_as_error

        assert(type(self.source_paths) is list)

        for path in self.source_paths:
            assert(os.path.exists(path))

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
            source_path=' '.join(self.source_paths),
            recursive="YES" if self.recursive else "NO",
            extra="")

        doxyfile_path = os.path.join(self.output_path, 'Doxyfile')
        with open(doxyfile_path, 'w') as doxyfile:

            doxyfile.write(doxyfile_content)

        # @todo: Doxygen generates a bunch of warnings. We should
        #        propagate these somehow - if you want to know what
        #        has not been documented etc.
        result = self.runner.run(
            command=self.doxygen_executable + ' Doxyfile',
            cwd=self.output_path)

        # Doxygen reports warnings on stderr. So if we have some output
        # there raise it.
        self._suppress_incorrect_warnings(result.stderr)

        if result.stderr.output and self.warnings_as_error:
            raise wurfapi.doxygen_error.DoxygenError(
                result.stderr.output)

        # The Doxygen XML is written to the 'xml' subfolder of the
        # output directory
        return os.path.join(self.output_path, 'xml')

    def _suppress_incorrect_warnings(self, stderr):

        # Sadly Doxygen outputs some incorrect warnings,
        # hopefully we won't break stuff.

        # Doxygen outputs a warning for enum class
        # Others report the same https://bit.ly/2uR2t5Z

        output = []

        for line in stderr.output:
            if 'warning: Internal inconsistency:' in line:
                continue
            else:
                output.append(line)

        stderr.output = output
