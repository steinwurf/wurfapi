import os
import functools
import operator
import jinja2


@jinja2.contextfilter
def api_filter(ctx, selectors, **attributes):

    result = []

    def match(element):
        for key, value in attributes.items():
            try:
                # This allows a user to write expressions such as:
                #
                #     selectors | api_filter(access=["private", "protected"])
                #
                # Which will then filter out all elements that are either
                # "private" or "protected"
                if (type(value) is list) and (element[key] in value):
                    continue

                if element[key] == value:
                    continue

                # None of the conditions matched so we break out
                return False
            except KeyError:
                return False
        return True

    for selector in selectors:
        element = ctx["api"][selector]

        if match(element):
            result.append(selector)

    return result


@jinja2.contextfilter
def api_sort(ctx, selectors, keys, reverse=False):
    # type: (jinja2.runtime.Context, List[str], List[str], bool) -> List[str]

    def compare(selector):
        # Get the nested value using approach described here:
        # https://stackoverflow.com/a/14692747/1717320
        return functools.reduce(operator.getitem, keys, ctx["api"][selector])

    # The sort should be stable
    return sorted(selectors, key=compare, reverse=reverse)


class TemplateRender(object):
    """ Finds the template on the file system with a given name. """

    def __init__(self, user_path):
        """ Create a new instance.

        :param user_path: The directory on the file system where the user
            provided templates are located as a string. If user_path is None
            no user specified templates will be loaded.
        """

        # We have two loaders either we load from the package
        # or from an user specified location
        loaders = []

        if user_path:
            assert os.path.isdir(user_path)

            loaders.append(
                jinja2.FileSystemLoader(searchpath=user_path))

        loaders.append(
            jinja2.PackageLoader(
                package_name='wurfapi', package_path='template_files'))

        self.environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(loaders=loaders),
            trim_blocks=True,
            lstrip_blocks=True,
            # Enable the do statement:
            # https://stackoverflow.com/a/39858522/1717320
            extensions=['jinja2.ext.do'])

        # self.environment.globals.update(
        #     rst_create_heading=rst_create_heading,
        #     rst_create_signature=rst_create_signature,
        #     api_filter=api_filter)

        self.environment.filters['api_sort'] = api_sort
        self.environment.filters['api_filter'] = api_filter

    def render(self, selector, api, filename, user_data=None):
        """ Render the template
        """

        template = self.environment.get_template(name=filename)
        params = {'api':api, 'selector':selector}
        if user_data is not None:
            params['user_data'] = user_data
        return template.render(**params)

