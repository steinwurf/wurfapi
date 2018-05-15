import os
import subprocess
import time

from . import compat
from . import check_output
from . import run_result
from . import run_error


def run(command, cwd, **kwargs):
    """Runs the command
    :param command: String or list of arguments
    :param cwd: The current working directory where the command will run
    :param kwargs: Keyword arguments passed to Popen(...)
    :return: A RunResult object representing the result of the command
    """

    if isinstance(command, compat.string_type):
        kwargs['shell'] = True

    if 'env' not in kwargs:
        # If 'env' is not passed as keyword argument use a copy of the
        # current environment.
        kwargs['env'] = os.environ.copy()

    if 'stdout' not in kwargs:
        kwargs['stdout'] = subprocess.PIPE

    if 'stderr' not in kwargs:
        kwargs['stderr'] = subprocess.PIPE

    assert 'cwd' not in kwargs
    kwargs['cwd'] = cwd

    start_time = time.time()

    popen = subprocess.Popen(
        command,
        # Need to decode the stdout and stderr with the correct
        # character encoding (http://stackoverflow.com/a/28996987)
        universal_newlines=True,
        **kwargs)

    stdout, stderr = popen.communicate()

    end_time = time.time()

    # The stdout and stderr are wrapped in a CheckOutput object to make
    # it easy to assert whether it contains specific data / strings.

    if stdout is not None:
        stdout = check_output.CheckOutput(output=stdout)

    if stderr is not None:
        stderr = check_output.CheckOutput(output=stderr)

    if isinstance(command, list):
        command = ' '.join(command)

    result = run_result.RunResult(
        command=command, path=cwd,
        stdout=stdout, stderr=stderr, returncode=popen.returncode,
        time=end_time - start_time)

    if popen.returncode != 0:
        raise run_error.RunError(result)

    return result
