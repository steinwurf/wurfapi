from . import wurfapi_error


class RunError(wurfapi_error.WurfapiError):
    """Basic exception for errors raised when running commands."""

    def __init__(self, run_result):
        super(RunError, self).__init__(str(run_result))
        self.run_result = run_result
