import os
import json
import sys
import io
import pprint
import difflib
import pytest


class Record(object):
    """ The Record object is a small test helper. Working similarly to
        vcrpy etc.

    You give it a recording path (filename) now when calling record(..)
    the following will happen:

    1. If a "recording" already suggests we check to see if the data
       matches
    2. If no "recording" exists we store it in the file.

    The file can be committed to version control. To accept a change in the
    output just delete the existing recording and make a new one.
    """

    def __init__(self, filename, recording_path, mismatch_path):
        """ Create a new instance.

        :param filename: The filename of the recording. Note the extension
            will determine the type of recorder used.
        :param recording_path: The directory to where the recording should
            be stored. E.g. /tmp/record note that typically recordings are
            put under version control.
        :param mismatch_path: The directory to where the mismatched
            recording should be stored. E.g. /tmp/mismatch note these should NOT
            be placed under version control.
        """

        assert os.path.isdir(recording_path)
        assert os.path.isdir(mismatch_path)

        _, extension = os.path.splitext(filename)

        if not extension in extension_map:
            raise NotImplementedError("We have no mapping for {}".format(
                extension))

        assert recording_path != mismatch_path

        recorder_cls = extension_map[extension]

        self.recorder = recorder_cls(filename=filename,
                                     recording_path=recording_path,
                                     mismatch_path=mismatch_path)

    def record(self, data):
        self.recorder.record(data=data)


class RecordError(Exception):
    """Basic exception for errors raised when running commands."""

    def __init__(self, filename, recording_path, recording_data, mismatch_path,
                 mismatch_data):

        recording_file = os.path.join(recording_path, filename)
        mismatch_file = os.path.join(mismatch_path, filename)

        # Unified diff expects a list of strings
        recording_lines = recording_data.split('\n')
        mismatch_lines = mismatch_data.split('\n')

        diff = difflib.unified_diff(
            a=recording_lines,
            b=mismatch_lines,
            fromfile=recording_file,
            tofile=mismatch_file)

        # unified_diff(...) returns a generator so we need to force the
        # data by interation - and then convert back to one string
        diff = "\n".join(list(diff))

        # Some differences are not easy to see with the unified diff console
        # output e.g. trailing white-spaces etc. So we also dump a HTML diff
        # output
        html_diff = difflib.HtmlDiff().make_file(
            fromlines=recording_lines,
            tolines=mismatch_lines,
            fromdesc=recording_file,
            todesc=mismatch_file)
        html_file = os.path.join(mismatch_path, 'diff.html')

        with io.open(html_file, 'w', encoding='utf-8') as html_fp:
            html_fp.write(html_diff)

        result = "Diff:\n{}\nHTML diff:\n{}".format(diff, html_file)

        super(RecordError, self).__init__(result)


class TextRecord(object):

    def __init__(self, filename, recording_path, mismatch_path):
        self.filename = filename
        self.recording_path = recording_path
        self.mismatch_path = mismatch_path

    def record(self, data):

        if sys.version_info < (3, 0):
            # Convert to unicode
            data = data.decode('utf-8')

        recording_file = os.path.join(self.recording_path, self.filename)
        mismatch_file = os.path.join(self.mismatch_path, self.filename)

        if not os.path.isfile(recording_file):

            with io.open(recording_file, 'w', encoding='utf-8') as recording_fp:
                recording_fp.write(data)

            return

        # A recording exists
        with io.open(recording_file, 'r', encoding='utf-8') as recording_fp:
            recording_data = recording_fp.read()

        assert type(recording_data) == type(data)
        if recording_data == data:
            return

        # There is a recording mismatch
        with io.open(mismatch_file, 'w', encoding='utf-8') as mismatch_fp:
            mismatch_fp.write(data)

        raise RecordError(
            filename=self.filename,
            recording_path=self.recording_path, recording_data=recording_data,
            mismatch_path=self.mismatch_path, mismatch_data=data)


class JsonRecord(TextRecord):

    def __init__(self, filename, recording_path, mismatch_path):
        super(JsonRecord, self).__init__(
            filename, recording_path, mismatch_path)

    def record(self, data):

        # Convert the data to json
        data = json.dumps(data, indent=2, sort_keys=True,
                          separators=(',', ': '))

        super(JsonRecord, self).record(data=data)


# Extension map for the different output files we support
extension_map = {
    '.json': JsonRecord,
    '.rst': TextRecord,
    '.txt': TextRecord
}
