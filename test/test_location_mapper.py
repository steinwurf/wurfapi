import pytest
import mock
import logging
import wurfapi.location_mapper


def test_location_mapper_to_include(caplog):
    caplog.set_level(logging.DEBUG)

    log = logging.getLogger(name='test_location_mapper_to_include')

    # No include paths
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root='/tmp/project_a', include_paths=[], log=log)

    assert mapper.to_include(
        path='/tmp/project_a/src/include/header.h') == None

    # In include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root='/tmp/project_a', include_paths=['/tmp/project_a/src/'],
        log=log)

    assert mapper.to_include(
        path='/tmp/project_a/src/include/header.h') == 'include/header.h'

    # Not in include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root='/tmp/project_a', include_paths=['/tmp/project_b/src/'],
        log=log)

    assert mapper.to_include(
        path='/tmp/project_a/src/include/header.h') == None

    # Not in first include path
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root='/tmp/project_a',
        include_paths=['/tmp/project_b/src/', '/tmp/project_a/src/'],
        log=log)

    assert mapper.to_include(
        path='/tmp/../tmp/project_a/./src/include/header.h') == 'include/header.h'


def test_location_mapper_to_path():

    log = mock.Mock()

    # Basic test
    mapper = wurfapi.location_mapper.LocationMapper(
        project_root='/tmp/project_a',
        include_paths=['/tmp/project_b/src/', '/tmp/project_a/src/'],
        log=log)

    assert mapper.to_path(
        path='/tmp/../tmp/project_a/./src/include/header.h') == 'src/include/header.h'

    with pytest.raises(RuntimeError):
        mapper.to_path('/tmp/project_b/helloworld.txt')
