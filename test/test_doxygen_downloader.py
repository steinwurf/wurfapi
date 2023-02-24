import mock
import os
import pytest
import shutil

import wurfapi
import wurfapi.doxygen_downloader


def test_doxygen_downloader_current_platform():

    assert wurfapi.doxygen_downloader.current_platform() in [
        "linux64",
        "win64",
        "win32",
    ]


@pytest.mark.download_test
def test_doxygen_downloader_download_linux(testdirectory):

    download_path = os.path.join(testdirectory.path(), "archive")

    executable = wurfapi.doxygen_downloader.doxygen_executable(
        from_path=download_path, platform="linux"
    )

    assert not os.path.isfile(executable)

    assert not wurfapi.doxygen_downloader.check_doxygen(
        platform="linux", download_path=download_path
    )

    downloaded_exectuable = wurfapi.doxygen_downloader.download_doxygen(
        download_path=download_path, platform="linux"
    )

    assert executable == downloaded_exectuable

    assert os.path.isfile(executable)

    if wurfapi.doxygen_downloader.current_platform() == "linux":
        testdirectory.run(executable + " --version")


@pytest.mark.download_test
def test_doxygen_downloader_download_win32(testdirectory):

    download_path = os.path.join(testdirectory.path(), "archive")

    wurfapi.doxygen_downloader.download_doxygen(
        download_path=download_path, platform="win32"
    )


@pytest.mark.download_test
def test_doxygen_downloader_download_win64(testdirectory):

    download_path = os.path.join(testdirectory.path(), "archive")

    wurfapi.doxygen_downloader.download_doxygen(
        download_path=download_path, platform="win64"
    )


@pytest.mark.ensure_doxygen
def test_doxygen_downloader_ensure_doxygen():

    default_path = wurfapi.doxygen_downloader.default_download_path()

    shutil.rmtree(default_path)

    executable = wurfapi.doxygen_downloader.ensure_doxygen()

    assert os.path.isfile(executable)
