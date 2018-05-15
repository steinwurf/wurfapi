import record
import pytest


def test_record_json(testdirectory):

    recording_path = testdirectory.mkdir('recording')
    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(filename='test.json',
                             recording_path=recording_path.path(),
                             mismatch_path=mismatch_path.path())

    recorder.record(data={'foo': 2, 'bar': 3})

    # Calling again with same data should be fine
    recorder.record(data={'foo': 2, 'bar': 3})
    recorder.record(data={'bar': 3, 'foo': 2})

    # With new data should raise
    with pytest.raises(record.RecordError):
        recorder.record(data={'foo': 3, 'bar': 3})


def test_record_rst(testdirectory):

    recording_path = testdirectory.mkdir('recording')
    mismatch_path = testdirectory.mkdir('mismatch')

    recorder = record.Record(filename='test.rst',
                             recording_path=recording_path.path(),
                             mismatch_path=mismatch_path.path())

    recorder.record(data="Hello\n=====\nWorld")

    # Calling again with same data should be fine
    recorder.record(data="Hello\n=====\nWorld")

    # With new data should raise
    with pytest.raises(record.RecordError):
        recorder.record(data="Hello\n=====\nwurfapi")


def test_record_no_mapping(testdirectory):

    recording_path = testdirectory.mkdir('recording')
    mismatch_path = testdirectory.mkdir('mismatch')

    with pytest.raises(NotImplementedError):

        recorder = record.Record(filename='test.tar.gz',
                                 recording_path=recording_path.path(),
                                 mismatch_path=mismatch_path.path())

        recorder.record(data="{'foo': 2, 'bar': 3}")
