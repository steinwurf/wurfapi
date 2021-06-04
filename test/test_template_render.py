import os
import mock
import json

import wurfapi
import wurfapi.doxygen_generator
import wurfapi.doxygen_parser
import wurfapi.template_render
import wurfapi.doxygen_downloader
import wurfapi.location_mapper

import record
import pytest_datarecorder


def generate_coffee_api(testdirectory):
    """Test helper - generate the XML."""

    output_dir = testdirectory.mkdir("xml_output")
    coffee_dir = testdirectory.copy_dir("test/data/cpp_coffee")
    src_dirs = [
        os.path.join(coffee_dir.path(), "src"),
        os.path.join(coffee_dir.path(), "examples", "header", "header.h"),
    ]

    doxygen_executable = wurfapi.doxygen_downloader.ensure_doxygen()

    generator = wurfapi.doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=wurfapi.run,
        recursive=True,
        source_paths=src_dirs,
        output_path=output_dir.path(),
        warnings_as_error=True,
    )

    xml_dir = generator.generate()

    log = mock.Mock()

    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=coffee_dir.path(), include_paths=src_dirs, log=log
    )

    reader = wurfapi.doxygen_parser.DoxygenParser(
        doxygen_path=xml_dir,
        location_mapper=mapper,
        patch_api=[
            {
                "selector": "project::v1_0_0::coffee::machine::impl",
                "key": "access",
                "value": "private",
            }
        ],
        log=log,
    )

    return reader.parse_index()


def test_template_finder_builtin(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    testdirectory.write_text(
        filename="api.json",
        data=json.dumps(api, indent=4, sort_keys=True),
        encoding="utf-8",
    )

    data = template.render(
        selector="project::v1_0_0::coffee::machine",
        api=api,
        filename="class_synopsis.rst",
    )

    testdirectory.write_text(filename="out.rst", data=data, encoding="utf-8")
    # testdirectory.run('rstcheck out.rst')

    mismatch_path = testdirectory.mkdir("mismatch")

    recorder = record.Record(
        filename="builtin_class_synopsis.rst",
        recording_path="test/data/template_recordings",
        mismatch_path=mismatch_path.path(),
    )

    recorder.record(data=data)


def test_template_finder_user(testdirectory):

    api = generate_coffee_api(testdirectory=testdirectory)

    user_path = testdirectory.copy_file("test/data/custom_templates/class_synopsis.rst")

    template = wurfapi.template_render.TemplateRender(user_path=testdirectory.path())

    data = template.render(selector=None, api=api, filename="class_synopsis.rst")

    expect = r"""custom coffee"""

    assert expect == data


def test_template_user_data(testdirectory):

    api = generate_coffee_api(testdirectory=testdirectory)

    user_path = testdirectory.copy_file("test/data/custom_templates/with_user_data.rst")

    template = wurfapi.template_render.TemplateRender(user_path=testdirectory.path())

    data = template.render(
        selector=None,
        api=api,
        filename="with_user_data.rst",
        user_data="123 user data user data 123",
    )

    expect = r"""123 user data user data 123"""

    assert expect == data

    data = template.render(selector=None, api=api, filename="with_user_data.rst")

    expect = r"""user_data is not defined"""

    assert expect == data


def test_template_render_namespace(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(
        selector="project::v1_0_0", api=api, filename="namespace_synopsis.rst"
    )

    mismatch_path = testdirectory.mkdir("mismatch")

    recorder = record.Record(
        filename="builtin_namespace_synopsis.rst",
        recording_path="test/data/template_recordings",
        mismatch_path=mismatch_path.path(),
    )

    recorder.record(data=data)


def test_template_render_enum(testdirectory):

    template = wurfapi.template_render.TemplateRender(user_path=None)

    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(
        selector="project::v1_0_0::coffee::mug_size",
        api=api,
        filename="enum_synopsis.rst",
    )

    mismatch_path = testdirectory.mkdir("mismatch")

    recorder = record.Record(
        filename="builtin_enum_synopsis.rst",
        recording_path="test/data/template_recordings",
        mismatch_path=mismatch_path.path(),
    )

    recorder.record(data=data)


def test_template_render_function(testdirectory, datarecorder):

    template = wurfapi.template_render.TemplateRender(user_path=None)
    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(
        selector="project::v1_0_0::print(doublea,int*b)",
        api=api,
        filename="function_synopsis.rst",
    )

    datarecorder.recording_path = (
        "test/data/template_recordings/builtin_function_synopsis.rst"
    )
    datarecorder.record(data=data)


def test_template_render_multiple_functions(testdirectory, datarecorder):

    template = wurfapi.template_render.TemplateRender(user_path=None)
    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(
        selector="project::v1_0_0", api=api, filename="function_synopsis.rst"
    )

    datarecorder.recording_path = (
        "test/data/template_recordings/builtin_multiple_function_synopsis.rst"
    )
    datarecorder.record(data=data)


def test_template_render_free_function(testdirectory, datarecorder):

    template = wurfapi.template_render.TemplateRender(user_path=None)
    api = generate_coffee_api(testdirectory=testdirectory)

    data = template.render(
        selector="version()", api=api, filename="function_synopsis.rst"
    )

    datarecorder.recording_path = (
        "test/data/template_recordings/builtin_free_function_synopsis.rst"
    )
    datarecorder.record(data=data)


template_string = """\
{%- from 'macros.rst' import escape_ref -%}
{{ escape_ref(data) }}
"""


def test_template_render_macro(datarecorder):

    render = wurfapi.template_render.TemplateRender(user_path=None)
    template = render.environment.from_string(template_string)
    data = template.render(data="<hello>")

    datarecorder.recording_path = "test/data/template_recordings/macro_escape_ref.rst"
    datarecorder.record(data=data)
