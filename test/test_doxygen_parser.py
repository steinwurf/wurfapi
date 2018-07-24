import pyquery
import os
import pprint
import mock
import logging

import wurfapi
import wurfapi.doxygen_parser
import wurfapi.doxygen_generator
import wurfapi.doxygen_downloader
import wurfapi.run

import record


def generate_coffee_xml(testdirectory):
    """ Test helper - generate the XML. """

    output_dir = testdirectory.mkdir('xml_output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')
    src_dir = coffee_dir.join('src')

    doxygen_executable = wurfapi.doxygen_downloader.ensure_doxygen()

    generator = wurfapi.doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=wurfapi.run,
        recursive=True,
        source_path=src_dir.path(),
        output_path=output_dir.path())

    return src_dir.path(), generator.generate()


def test_coffee(testdirectory, caplog):

    caplog.set_level(logging.DEBUG)

    src_dir, xml_dir = generate_coffee_xml(testdirectory)
    log = logging.getLogger(name='test_coffee')

    parser = wurfapi.doxygen_parser.DoxygenParser(
        doxygen_path=xml_dir, project_path=src_dir, log=log)

    api = parser.parse_index()

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='coffee.json',
        recording_path='test/data/parser_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=api)


def generate_xml(testdirectory, source_file):
    """ Test helper - generate the XML. """

    output_dir = testdirectory.mkdir('xml_output')
    source_dir = testdirectory.mkdir('sources')
    source_dir.copy_file(source_file)

    doxygen_executable = wurfapi.doxygen_downloader.ensure_doxygen()

    generator = wurfapi.doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=wurfapi.run,
        recursive=True,
        source_path=source_dir.path(),
        output_path=output_dir.path())

    return source_dir.path(), generator.generate()


def test_parser_input_function(testdirectory, caplog):

    caplog.set_level(logging.DEBUG)

    src_dir, xml_dir = generate_xml(
        testdirectory,
        source_file='test/data/parser_input/function.hpp')

    log = logging.getLogger(name='test_parser_input_function')

    parser = wurfapi.doxygen_parser.DoxygenParser(
        doxygen_path=xml_dir, project_path=src_dir, log=log)

    api = parser.parse_index()

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='parser_input_function.json',
        recording_path='test/data/parser_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=api)


def test_parser_replace_with():

    data_in = {
        'a': {'b': 'replace', 'c': ['replace', {'a': 'replace'}]}
    }

    data_out = wurfapi.doxygen_parser.replace_with(
        {'replace': 'with'}, data_in
    )

    data_expect = {
        'a': {'b': 'with', 'c': ['with', {'a': 'with'}]}
    }

    assert data_out == data_expect
