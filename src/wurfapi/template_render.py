import os
import jinja2


def rst_create_heading(name, character):
    """ @todo document these helpers"""
    return name + '\n' + character*len(name)


def rst_create_signature(unique_name, function):

    signature = ":ref:`" + function["name"] + "<" + unique_name + ">` "
    signature += "**(** "

    parameters = []
    for p in function["parameters"]:
        parameters.append(p["type"] + " " + p["name"])

    signature += ", ".join(parameters)
    signature += " **)**"

    return signature


def api_filter(api, selectors, **attributes):

    result = []

    def match(element):
        for key, value in attributes.items():
            try:
                if value != element[key]:
                    return False
            except KeyError:
                return False
        return True

    for selector in selectors:
        element = api[selector]

        if match(element):
            result.append(selector)

    return result


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
            # Enable the do statement:
            # https://stackoverflow.com/a/39858522/1717320
            extensions=['jinja2.ext.do'])

        self.environment.globals.update(
            rst_create_heading=rst_create_heading,
            rst_create_signature=rst_create_signature,
            api_filter=api_filter)

    def render(self, selector, api, filename):
        """ Render the template
        """

        template = self.environment.get_template(name=filename)
        return template.render(api=api, selector=selector)
