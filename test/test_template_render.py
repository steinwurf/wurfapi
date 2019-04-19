import os
import mock

import wurfapi
import wurfapi.doxygen_generator
import wurfapi.doxygen_parser
import wurfapi.template_render
import wurfapi.doxygen_downloader

import record
import pytest_datarecorder


def generate_coffee_api(testdirectory):
    """ Test helper - generate the XML. """

    output_dir = testdirectory.mkdir('xml_output')
    coffee_dir = testdirectory.copy_dir('test/data/cpp_coffee')
    src_dirs = [os.path.join(coffee_dir.path(), 'src'), os.path.join(
        coffee_dir.path(), 'examples', 'header', 'header.h')]

    doxygen_executable = wurfapi.doxygen_downloader.ensure_doxygen()

    generator = wurfapi.doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=wurfapi.run,
        recursive=True,
        source_paths=src_dirs,
        output_path=output_dir.path(),
        warnings_as_error=True)

    xml_dir = generator.generate()

    log = mock.Mock()

    reader = wurfapi.doxygen_parser.DoxygenParser(
        doxygen_path=xml_dir,
        project_paths=src_dirs,
        patch_api=[
            {'selector': 'project::coffee::machine::impl',
                'key': 'access', 'value': 'private'}],
        log=log)

    return reader.parse_index()


def test_template_finder_builtin(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(selector="project::coffee::machine", api=api,
                           filename='class_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_class_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)


def test_template_finder_user(testdirectory):

    api = generate_coffee_api(testdirectory=testdirectory)

    user_path = testdirectory.copy_file(
        'test/data/custom_templates/class_synopsis.rst')

    template = wurfapi.template_render.TemplateRender(
        user_path=testdirectory.path())

    data = template.render(selector=None, api=api,
                           filename='class_synopsis.rst')

    expect = r"""custom coffee"""

    assert expect == data


def test_template_render_namespace(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(selector='project', api=api,
                           filename='namespace_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_namespace_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)


def test_template_render_enum(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(selector='project::coffee::mug_size', api=api,
                           filename='enum_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_enum_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)


def test_template_render_function(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(selector='project::print(double,int*)', api=api,
                           filename='function_synopsis.rst')

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='builtin_function_synopsis.rst',
        recording_path='test/data/template_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=data)


template_string = """\
{%- from 'macros.rst' import escape_ref -%}
{{ escape_ref(data) }}
"""


def test_template_render_macro(datarecorder):

    datarecorder.recording_path = "test/data/template_recordings/macro_escape_ref.rst"

    render = wurfapi.template_render.TemplateRender(user_path=None)
    template = render.environment.from_string(template_string)
    output = template.render(data="<hello>")

    datarecorder.record(data=output)
