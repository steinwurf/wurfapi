import sys

IS_PY2 = sys.version_info[0] == 2

if IS_PY2:
    string_type = basestring
else:
    string_type = str
