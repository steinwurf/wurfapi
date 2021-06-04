import os

import wurfapi
import wurfapi.run


def test_run(testdirectory):
    wurfapi.run.run("python --version", cwd=testdirectory.path())
