from . import wurfapi_error


class DoxygenError(wurfapi_error.WurfapiError):
    """Error running Doxygen."""

    def __init__(self, errors):

        message = "Doxygen Error:\n"
        for error in errors:
            message += "\n{}\n".format(error)

        message += "\nTotal errors {}\n".format(len(errors))

        super(DoxygenError, self).__init__(message)
