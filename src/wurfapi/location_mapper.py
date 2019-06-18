import os


class LocationMapper(object):

    def __init__(self, project_root, include_paths):
        # type: (str, List[str]) -> None
        """ Instantiate new object

        :param project_root: Absolute path to the root of the project as a
            string.
        :param include_paths: List of absolute include paths as strings
        """

        self.project_root = project_root
        self.include_paths = include_paths

        assert os.path.isabs(self.project_root)

        for include_path in self.include_paths:
            assert os.path.isabs(include_path)

    def to_include(self, path):
        # type: (str) -> Optional[str]
        """
        :param path: The path to a file as a string.
        :return: The include directive if file found in the include paths
        """

        # Remove any redundant path elements
        path = self._expand_path(path=path)

        for include_path in self.include_paths:

            relative_path = self._relative_path(path=path, start=include_path)

            if relative_path:
                return relative_path

        return None

    def to_path(self, path):
        # type: (str) -> str
        """
        :param path: The path to the file as a string
        :return: The relative path to the file from the project root
        """

        # Remove any redundant path elements
        path = self._expand_path(path=path)

        relative_path = self._relative_path(path=path, start=self.project_root)

        if not relative_path:
            raise RuntimeError(
                "File {} not contained in project root {}".format(path, self.project_root))

        return relative_path

    def _relative_path(self, path, start):

        if not path.startswith(start):
            return None

        # Otherwise we return the relative path from the
        # project path
        path = os.path.relpath(path=path, start=start)

        # Make sure we use unix / linux style paths - also on windows
        path = path.replace('\\', '/')

        return path

    def _expand_path(self, path):
        # Remove any redundant path elements
        path = os.path.normpath(path)
        path = os.path.expanduser(path)
        return os.path.abspath(path)
