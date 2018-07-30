import os
import sys

import docutils.nodes
import docutils.parsers
import docutils.parsers.rst
import docutils.parsers.rst.directives
import docutils.statemachine

import sphinx
import sphinx.util
import sphinx.util.logging
import sphinx.util.nodes

import pyquery
import json
import logging

from . import doxygen_generator
from . import doxygen_parser
from . import doxygen_downloader
from . import run
from . import template_render
from . import wurfapi_error

VERSION = '2.1.0'


class WurfapiDirective(docutils.parsers.rst.Directive):

    # The wurfapiDirective requires a single path argument, which is allowed to
    # contain whitepace. This is to allow for long paths which may span
    # multiple lines. The path argument should name a valid template.
    #
    # Same approach as for the image directive:
    # http://docutils.sourceforge.net/docs/howto/rst-directives.html#id10
    required_arguments = 1
    final_argument_whitespace = True

    # A selector may be specified. Some templates may require it. @todo
    # document how to handle situations where:
    # 1. A selector is not needed but passed
    # 2. A selector is needed but not passed
    option_spec = {
        # unchanged: Returns the text argument, unchanged. Returns an empty
        # string ("") if no argument is found.
        'selector': docutils.parsers.rst.directives.unchanged
    }

    def run(self):
        """ Called by Sphinx.

        Process the directive.

        Documentation on creating directives are available here:
        http://docutils.sourceforge.net/docs/howto/rst-directives.html

        :return: List of Docutils/Sphinx nodes that will be inserted into the
                 document where the directive was encountered.
        """

        # The path function returns the path argument unwrapped (with newlines
        # removed). Raises ValueError if no argument is found.
        template_path = docutils.parsers.rst.directives.path(self.arguments[0])

        env = self.state.document.settings.env
        app = env.app
        api = app.wurfapi_api
        selector = self.options["selector"]

        if selector not in api:
            raise wurfapi_error.WurfapiError(
                'Selector "{}" not in API possible values are {}'.format(
                    selector, api.keys()))

        template = template_render.TemplateRender(user_path=None)

        data = template.render(
            selector=self.options['selector'], api=app.wurfapi_api,
            filename=template_path)

        return self.insert_rst(data)

    def insert_rst(self, rst):
        """ Replaces the content of the directive with the rst generated
            content.

        Documentation on how to do this is available here:
        http://www.sphinx-doc.org/en/stable/extdev/markupapi.html
        """
        rst = rst.split('\n')
        view = docutils.statemachine.ViewList(initlist=rst, source="wurfapi")

        node = docutils.nodes.paragraph()
        sphinx.util.nodes.nested_parse_with_titles(
            state=self.state, content=view, node=node)

        return node.children


def main():

    print("hello wurfapi")


def generate_doxygen(app):

    source_path = os.path.join(app.srcdir,
                               app.config.wurfapi['source_path'])

    output_path = os.path.join(app.doctreedir, 'wurfapi')

    if not os.path.exists(output_path):
        os.makedirs(name=output_path)

    # Sphinx colorizes the log output differently on windows and linux
    # so we manually create a logger which, like sphinx, sends anything
    # below debug to stdout and above to stderr
    logger = sphinx.util.logging.getLogger('wurfapi')

    # class LessThanFilter(logging.Filter):
    #     def __init__(self, exclusive_maximum, name=""):
    #         super(LessThanFilter, self).__init__(name)
    #         self.max_level = exclusive_maximum

    #     def filter(self, record):
    #         # non-zero return means we log this message
    #         return 1 if record.levelno < self.max_level else 0

    # # Have to set the root logger level, it defaults to logging.WARNING
    # logger.setLevel(logging.NOTSET)

    # logging_handler_out = logging.StreamHandler(sys.stdout)
    # logging_handler_out.setLevel(logging.DEBUG)
    # logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    # logger.addHandler(logging_handler_out)

    # logging_handler_err = logging.StreamHandler(sys.stderr)
    # logging_handler_err.setLevel(logging.WARNING)
    # logger.addHandler(logging_handler_err)

    logger.info('wurfapi source_path={} output_path={}'.format(
        source_path, output_path))

    parser = app.config.wurfapi['parser']
    assert parser['type'] == 'doxygen'

    if parser['download']:

        if 'download_path' in parser:
            download_path = parser['download_path']
        else:
            download_path = None

        doxygen_executable = doxygen_downloader.ensure_doxygen(
            download_path=download_path)
    else:
        doxygen_executable = 'doxygen'

    generator = doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=run,
        recursive=True,
        source_path=source_path,
        output_path=output_path,
        warnings_as_error=parser['warnings_as_error'])

    output = generator.generate()

    logger.info('wurfapi doxygen XML {}'.format(output))

    parser = doxygen_parser.DoxygenParser(
        doxygen_path=output, project_path=source_path, log=logger)

    app.wurfapi_api = parser.parse_index()

    with open(os.path.join(output_path, 'wurfapi_api.json'), 'w') as f:
        json.dump(app.wurfapi_api, f)


def setup(app):
    """ Entry point for the extension. Sphinx will call this function when the
        module is added to the "extensions" list in Sphinx's conf.py file.

        :param app: The application object, which is an instance of Sphinx.
    """

    # Create a logger
    logger = sphinx.util.logging.getLogger('wurfapi')
    logger.info('Initializing wurfapi extension')

    # Add the wurfapi configuration value
    app.add_config_value(name='wurfapi', default=None, rebuild=True)

    # Add the new directive - added to the document by writing:
    #
    #    ..wurfapi::
    #
    app.add_directive(name='wurfapi', obj=WurfapiDirective)

    # Generate the XML
    app.connect(event="builder-inited", callback=generate_doxygen)

    # We use the doctreedir as build directory. The default for this
    # is inside _build/.doctree folder
    build_dir = os.path.join(app.doctreedir, 'wurfapi')

    # Run Doxygen on the source code

    return {'version': VERSION}
