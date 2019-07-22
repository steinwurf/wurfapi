#! /usr/bin/env python
# encoding: utf-8

from waflib.Build import BuildContext
import os
import sys
import shutil
import hashlib
import subprocess

from waflib.Configure import conf
from waflib import Logs

import waflib

top = '.'

VERSION = '2.2.0'


class UploadContext(BuildContext):
    cmd = 'upload'
    fun = 'upload'


def options(opt):

    opt.add_option(
        '--run_tests', default=False, action='store_true',
        help='Run all unit tests')

    opt.add_option(
        '--pytest_basetemp', default='pytest_temp',
        help='Set the prefix folder where pytest executes the tests')

    opt.add_option(
        '--run_download_tests', default=False, action='store_true',
        help='Run the unit tests that use network resources'
        ' (downloading Doxygen')

    opt.add_option(
        '--run_ensure_doxygen', default=False, action='store_true',
        help='Ensure that doxygen is available (will retrieve a fresh copy)')

    opt.add_option(
        '--test_filter', default=None, action='store',
        help='Runs all tests that include the substring specified.'
             'Wildcards not allowed. (Used with --run_tests)')


def build(bld):

    # Create a virtualenv in the source folder and build universal wheel
    # Make sure the virtualenv Python module is in path
    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:
        venv.pip_install(packages=['wheel'])
        venv.run(cmd='python setup.py bdist_wheel --universal', cwd=bld.path)

    # Delete the egg-info directory, do not understand why this is created
    # when we build a wheel. But, it is - perhaps in the future there will
    # be some way to disable its creation.
    egg_info = os.path.join('src', 'wurfapi.egg-info')

    if os.path.isdir(egg_info):
        waflib.extras.wurf.directory.remove_directory(path=egg_info)

    # Run the unit-tests
    if bld.options.run_tests:
        _pytest(bld=bld)


def _find_wheel(ctx):
    """ Find the .whl file in the dist folder. """

    wheel = ctx.path.ant_glob('dist/*-'+VERSION+'-*.whl')

    if not len(wheel) == 1:
        ctx.fatal('No wheel found (or version mismatch)')
    else:
        wheel = wheel[0]
        Logs.info('Wheel %s', wheel)
        return wheel


def upload(bld):
    """ Upload the built wheel to PyPI (the Python Package Index) """

    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:
        venv.pip_install(packages=['twine'])

        wheel = _find_wheel(ctx=bld)

        venv.run('python -m twine upload {}'.format(wheel))


def _pytest(bld):

    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:

        venv.run('python -m pip install pytest')
        venv.run('python -m pip install pytest-testdirectory')
        venv.run('python -m pip install sphinx')
        venv.run('python -m pip install mock')
        venv.run('python -m pip install vcrpy')
        venv.run('python -m pip install '
                 'git+https://github.com/steinwurf/pytest-datarecorder.git@'
                 '6a2c106c1a7f08236fcdd7b1b8742b010ec2403e')

        # Install the pytest-testdirectory plugin in the virtualenv
        wheel = _find_wheel(ctx=bld)

        venv.run('python -m pip install {}'.format(wheel))

        # We override the pytest temp folder with the basetemp option,
        # so the test folders will be available at the specified location
        # on all platforms. The default location is the "pytest" local folder.
        basetemp = os.path.abspath(os.path.expanduser(
            bld.options.pytest_basetemp))

        # We need to manually remove the previously created basetemp folder,
        # because pytest uses os.listdir in the removal process, and that fails
        # if there are any broken symlinks in that folder.
        if os.path.exists(basetemp):
            waflib.extras.wurf.directory.remove_directory(path=basetemp)

        testdir = bld.path.find_node('test')

        # Make the basetemp directory
        os.makedirs(basetemp)

        # Main test command
        command = 'python -B -m pytest {} --basetemp {}'.format(
            testdir.abspath(), os.path.join(basetemp, 'unit_tests'))

        # Skip the tests that have the "download_test" marker
        command += ' -m "not download_test and not ensure_doxygen"'

        # Adds the test filter if specified
        if bld.options.test_filter:
            command += ' -k "{}"'.format(bld.options.test_filter)

        # Make python not write any .pyc files. These may linger around
        # in the file system and make some tests pass although their .py
        # counter-part has been e.g. deleted
        venv.run(cmd=command, cwd=bld.path)

        if bld.options.run_download_tests:
            # Main test command
            command = 'python -B -m pytest {} --basetemp {}'.format(
                testdir.abspath(), os.path.join(basetemp, 'download_tests'))

            # Skip the tests that have the "download_test" marker
            command += ' -m "download_test"'

            # Make python not write any .pyc files. These may linger around
            # in the file system and make some tests pass although their .py
            # counter-part has been e.g. deleted
            venv.run(cmd=command, cwd=bld.path)

        if bld.options.run_ensure_doxygen:
            # Main test command
            command = 'python -B -m pytest {} --basetemp {}'.format(
                testdir.abspath(), os.path.join(basetemp, 'ensure_doxygen'))

            # Skip the tests that have the "download_test" marker
            command += ' -m "ensure_doxygen"'

            # Make python not write any .pyc files. These may linger around
            # in the file system and make some tests pass although their .py
            # counter-part has been e.g. deleted
            venv.run(cmd=command, cwd=bld.path)

        # Check readme
        # https://stackoverflow.com/a/49107899/1717320
        venv.run(cmd='python setup.py check -r -s', cwd=bld.path)

        venv.pip_install(['collective.checkdocs'])
        venv.run(cmd='python setup.py checkdocs', cwd=bld.path)


class ReleaseContext(BuildContext):
    cmd = 'prepare_release'
    fun = 'prepare_release'


def prepare_release(ctx):
    """ Prepare a release. """

    # Rewrite version
    with ctx.rewrite_file(filename="src/wurfapi/wurfapi_directive.py") as f:
        pattern = r"VERSION = '\d+\.\d+\.\d+'"
        replacement = "VERSION = '{}'".format(VERSION)

        f.regex_replace(pattern=pattern, replacement=replacement)
