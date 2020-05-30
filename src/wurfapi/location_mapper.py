import os

try:
    import pathlib
except (ImportError):
    import pathlib2 as pathlib


class LocationMapper(object):

    def __init__(self, project_root, include_paths, log):
        # type: (str, List[str]) -> None
        """ Instantiate new object

        :param project_root: Absolute path to the root of the project as a
            string.
        :param include_paths: List of absolute include paths as strings
        """

        self.project_root = pathlib.Path(project_root).resolve()
        self.include_paths = [pathlib.Path(p).resolve() for p in include_paths]
        self.log = log

    def to_include(self, path):
        # type: (str) -> Optional[str]
        """
        :param path: The path to a file as a string.
        :return: The include directive if file found in the include paths
        """
        path = pathlib.Path(path)

        if not path.is_absolute():
            path = self.project_root.joinpath(path)

        path = path.resolve()

        for include_path in self.include_paths:

            relative_path = self._relative_path(path=path, start=include_path)

            if relative_path:
                return relative_path

        self.log.debug("Unable to find file %s in includes %s", path,
                       self.include_paths)

        return None

    def to_path(self, path):
        # type: (str) -> str
        """
        :param path: The path to the file as a string
        :return: The relative path to the file from the project root
        """

        path = pathlib.Path(path)

        if not path.is_absolute():
            path = self.project_root.joinpath(path)

        path = path.resolve()

        relative_path = self._relative_path(path=path, start=self.project_root)

        if not relative_path:
            raise RuntimeError(
                "File {} not contained in project root {}".format(path, self.project_root))

        return relative_path

    def _relative_path(self, path, start):

        if start not in path.parents:
            return None

        # Otherwise we return the relative path from the
        # project path
        relative_path = path.relative_to(start)

        # Make sure we use unix / linux style paths - also on windows
        relative_path = str(relative_path).replace('\\', '/')

        return relative_path
