import os

import record


def test_run(testdirectory):

    testdirectory.run('python -m wurfapi')
    testdirectory.run('wurfapi')


def test_build_docs(testdirectory):

    cpp_coffee = testdirectory.copy_dir(directory='test/data/cpp_coffee')

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
