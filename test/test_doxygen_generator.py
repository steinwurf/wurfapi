import mock
import os

import wurfapi
import wurfapi.doxygen_generator
import wurfapi.doxygen_downloader
import wurfapi.run


def test_doxygen_generator(testdirectory):

    output_dir = testdirectory.mkdir('output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')

    runner = mock.Mock()

    doxygen_executable = wurfapi.doxygen_downloader.ensure_doxygen()

    generator = wurfapi.doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=wurfapi.run,
        recursive=True,
        source_path=coffee_dir.path(),
        output_path=output_dir.path(),
        warnings_as_error=True)

    xml_output = generator.generate()

    assert output_dir.contains_file('Doxyfile')

    index_xml = os.path.join(xml_output, 'index.xml')
    assert os.path.isfile(index_xml)
