#! /usr/bin/env python
# encoding: utf-8

import cgi
import os
import sys
import archive

from .compat import IS_PY2
from .wurfapi_error import WurfapiError

if IS_PY2:

    # Python 2
    from urllib2 import urlopen
    from urlparse import urlparse
else:

    # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlparse

# Example URLs:
#
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.linux.bin.tar.gz
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.windows.bin.zip
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.windows.x64.bin.zip

BASE_URL = "https://sourceforge.net/projects/doxygen/files/rel-1.8.12/"

# Version 1.8.13 segfaults if the C++ code has any friend declarations
# as described here:
# https://bugzilla.gnome.org/show_bug.cgi?id=777941
# This regression was fixed here:
# https://bugzilla.gnome.org/show_bug.cgi?id=776791

# Version 1.8.14 has a broken Linux binary:
# https://bugzilla.gnome.org/show_bug.cgi?id=792761
# it is linked with libclang but does not ship with it, so you get the following
# error:
#
#     doxygen: error while loading shared libraries: libclang.so.6: cannot
#     open shared object file: No such file or directory
#
# Running ldd gives:
#
#   linux-vdso.so.1 =>  (0x00007ffc883a8000)
#   libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f39d96e3000)
#   libclang.so.6 => not found
#   libtinfo.so.5 => /lib/x86_64-linux-gnu/libtinfo.so.5 (0x00007f39d94ba000)
#   libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f39d929d000)
#   libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f39d8f17000)
#   libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f39d8bc1000)
#   libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f39d89aa000)
#   libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f39d85ca000)
#   /lib64/ld-linux-x86-64.so.2 (0x00007f39d9902000)

VERSION = "1.8.12"

class DoxygenUnsupportedError(WurfapiError):

    def __init__(self, platform):
        msg = "Unsupported platform for doxygen auto download {}\n".format(
            platform)

        msg += "See README.rst at github.com/steinwurf/wurfapi on how\n"
        msg += "to install Doxygen on your system and use that."

        super(DoxygenUnsupportedError, self).__init__(msg)


def current_platform():

    if sys.platform.startswith('linux'):
        # Checking for 64 bit
        # https://docs.python.org/3/library/platform.html#cross-platform

        if sys.maxsize > 2**32:
            return "linux64"
        else:
            return "linux32"

    if sys.platform.startswith('win'):

        # Checking for 64 bit
        # https://docs.python.org/3/library/platform.html#cross-platform

        if sys.maxsize > 2**32:
            return "win64"
        else:
            return "win32"

    raise DoxygenUnsupportedError(sys.platform)


def archive_name(platform):

    if platform == 'linux64':
        return 'doxygen-' + VERSION + '.linux.bin.tar.gz'

    if platform == 'win32':
        return 'doxygen-' + VERSION + '.windows.bin.zip'

    if platform == 'win64':
        return 'doxygen-' + VERSION + '.windows.x64.bin.zip'

    raise DoxygenUnsupportedError(platform)


def doxygen_executable(from_path, platform):

    if platform == 'linux64':
        return os.path.join(from_path, 'doxygen-' + VERSION, 'bin/doxygen')

    if platform == 'win32':
        return os.path.join(from_path, 'doxygen.exe')

    if platform == 'win64':
        return os.path.join(from_path, 'doxygen.exe')

    raise DoxygenUnsupportedError(platform)


def doxygen_url(platform):
    return os.path.join(BASE_URL, archive_name(platform))


def default_download_path():

    # https://stackoverflow.com/a/4028943
    home_path = os.path.join(os.path.expanduser("~"))
    return os.path.join(home_path, '.wurfapi', 'local-doxygen', VERSION)


def download_archive(url, to_path):
    """ Download the file specified by the source.
    :param cwd: The directory where to download the file.
    :param url: The URL of the file to download.
    :param filename: The filename to store the file under.
    """

    response = urlopen(url=url)

    # From http://stackoverflow.com/a/1517728
    CHUNK = 16 * 1024
    with open(to_path, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)


def extract_archive(from_path, to_path):

    assert os.path.isfile(from_path)

    archive.extract(path=from_path, to_path=to_path)

    return to_path


def download_doxygen(platform=None, download_path=None):

    if platform == None:
        platform = current_platform()

    # Where to download the archive
    if download_path == None:
        download_path = default_download_path()

    if not os.path.isdir(download_path):
        os.makedirs(download_path)

    archive_path = os.path.join(download_path, archive_name(platform))

    url = doxygen_url(platform=platform)

    download_archive(url=url, to_path=archive_path)

    extract_archive(from_path=archive_path, to_path=download_path)

    executable = doxygen_executable(from_path=download_path, platform=platform)

    assert os.path.isfile(executable)

    return executable


def check_doxygen(platform=None, download_path=None):

    if platform == None:
        platform = current_platform()

    if download_path == None:
        download_path = default_download_path()

    executable = doxygen_executable(from_path=download_path, platform=platform)

    return os.path.isfile(executable)


def ensure_doxygen(platform=None, download_path=None):

    if platform == None:
        platform = current_platform()

    if download_path == None:
        download_path = default_download_path()

    if check_doxygen(platform=platform, download_path=download_path):
        return doxygen_executable(platform=platform, from_path=download_path)
    else:
        return download_doxygen(platform=platform, download_path=download_path)
