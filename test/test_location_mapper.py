import pytest
import mock
import os
import logging
import wurfapi.location_mapper

try:
    import pathlib
except (ImportError):
    import pathlib2 as pathlib


def test_location_mapper_to_include(testdirectory, caplog):
    caplog.set_level(logging.DEBUG)

    log = logging.getLogger(name='test_location_mapper_to_include')

    project_dir = pathlib.Path(testdirectory.copy_dir(
        directory='test/data/location_mapper').path())

    # No include paths
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=project_dir / "tmp/tmp/project_a", include_paths=[], log=log)

    assert mapper.to_include(
        path=project_dir / "tmp/project_a/src/include/header.h") == None

    # In include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=project_dir / "tmp/project_a",
        include_paths=[project_dir / "tmp/project_a/src"],
        log=log)

    assert mapper.to_include(
        path=project_dir / "tmp/project_a/src/include/header.h") == 'include/header.h'

    # Not in include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=project_dir / "tmp/project_a",
        include_paths=[project_dir / "tmp/project_b/src"],
        log=log)

    assert mapper.to_include(
        path=project_dir / "tmp/project_a/src/include/header.h") == None

    # Not in first include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=project_dir / "tmp/project_a",
        include_paths=[project_dir / "tmp/project_b/src",
                       project_dir / "tmp/project_a/src"],
        log=log)

    assert mapper.to_include(
        path=project_dir / "tmp/project_a/src/include/header.h") == 'include/header.h'


def test_location_mapper_to_path(testdirectory):

    log = mock.Mock()

    project_dir = pathlib.Path(testdirectory.copy_dir(
        directory='test/data/location_mapper').path())

    # Basic test
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root=project_dir / "tmp/project_a",
        include_paths=[project_dir / "tmp/project_b/src",
                       project_dir / "tmp/project_a/src"],
        log=log)

    assert mapper.to_path(
        path=project_dir / 'tmp/../tmp/project_a/./src/include/header.h') == 'src/include/header.h'

    with pytest.raises(RuntimeError):
        mapper.to_path(path=project_dir / 'tmp/project_b/helloworld.txt')
