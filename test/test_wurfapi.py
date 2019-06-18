import os
import json

import record


def test_run(testdirectory):

    testdirectory.run('python -m wurfapi')
    testdirectory.run('wurfapi')


def test_build_docs(testdirectory):

    cpp_coffee = testdirectory.copy_dir(directory='test/data/cpp_coffee')

    # Make it a git repo - we will try to fetch the project root from git
    cpp_coffee.run(['git', 'init'])
    cpp_coffee.run(['git', 'add', '.'])
    cpp_coffee.run(['git', '-c', 'user.name=John', '-c',
                    'user.email=doe@email.org', 'commit', '-m', 'oki'])

    docs = cpp_coffee.join('docs')
    docs.run('sphinx-build --no-color -w log.txt -b html . _build')

    log_file = os.path.join(docs.path(), 'log.txt')

    # The log file should have zero size - i.e. now warnings or errors..
    # As you can see we are not quite there :)
    with open(log_file, 'r') as log:
        log_data = log.read()

    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(
        filename='log.txt',
        recording_path='test/data/log_recordings',
        mismatch_path=mismatch_path.path())

    recorder.record(data=log_data)

    # Find and track changes to the wurfapi json file. This is the final API
    # output produced after parsing the sources and running our various steps
    # to transform the output.
    wurfapi_json_file = os.path.join(
        docs.path(), '_build', '.doctrees', 'wurfapi_api.json')

    recorder = record.Record(
        filename='build_coffee_wurfapi.json',
        recording_path='test/data/',
        mismatch_path=mismatch_path.path())

    with open(wurfapi_json_file, 'r') as wurfapi_json:
        data = json.load(wurfapi_json)

    recorder.record(data=data)
