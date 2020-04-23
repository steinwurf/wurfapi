import os
import sys
import hashlib
import tempfile
import shutil

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
from . import link_mapper
from . import link_provider
from . import location_mapper
from . import check_api_schema
from . import collapse_inline_namespaces


VERSION = '6.0.0'


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
        user_path = app.config.wurfapi.get('user_templates', None)

        if user_path:
            # Make sure it is relative to the documentation directory
            user_path = os.path.join(app.srcdir, user_path)

        if selector not in api:
            raise wurfapi_error.WurfapiError(
                'Selector "{}" not in API possible values are {}'.format(
                    selector, api.keys()))

        template = template_render.TemplateRender(user_path=user_path)

        data = template.render(
            selector=self.options['selector'], api=app.wurfapi_api,
            filename=template_path)

        # Dump the rst to a file - mostly for debugging purposes
        rst_file = "".join([x for x in selector if x.isalnum()]) + ".rst"
        rst_path = os.path.join(app.wurfapi_output_path, rst_file)
        with open(rst_path, 'w') as f:
            f.write(data)

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
    # This is intentional don't delete.
    print("hello wurfapi")


def generate_doxygen(app):

    source_paths = []
    for source_path in app.config.wurfapi['source_paths']:

        source_path = os.path.join(app.srcdir, source_path)

        if not os.path.exists(source_path):
            raise RuntimeError("Missing source path {}".format(source_path))

        source_paths.append(source_path)

    # Create the XML in a temp location
    project = app.config.project.lower() if app.config.project else ""
    # Remove whitespace https://stackoverflow.com/a/2077944/1717320
    project = "_".join(project.split())

    source_hash = hashlib.sha1(
        ",".join(source_paths).encode('utf-8')).hexdigest()[:6]

    output_path = os.path.join(
        tempfile.gettempdir(), "wurfapi-"+project+"-"+source_hash)

    if os.path.isdir(output_path):
        shutil.rmtree(output_path, ignore_errors=True)

    if not os.path.exists(output_path):
        os.makedirs(name=output_path)

    # Store the output path
    app.wurfapi_output_path = output_path

    # Sphinx colorizes the log output differently on windows and linux
    # so we manually create a logger which, like sphinx, sends anything
    # below debug to stdout and above to stderr
    logger = sphinx.util.logging.getLogger('wurfapi')

    logger.info('wurfapi source_path={} output_path={}'.format(
        source_paths, output_path))

    parser_config = app.config.wurfapi['parser']
    assert parser_config['type'] == 'doxygen'

    if parser_config['download']:

        if 'download_path' in parser_config:
            download_path = parser_config['download_path']
        else:
            download_path = None

        doxygen_executable = doxygen_downloader.ensure_doxygen(
            download_path=download_path)
    else:
        doxygen_executable = 'doxygen'

    # Check if we should be recursive
    recursive = app.config.wurfapi['recursive']

    generator = doxygen_generator.DoxygenGenerator(
        doxygen_executable=doxygen_executable,
        runner=run,
        recursive=recursive,
        source_paths=source_paths,
        output_path=output_path,
        warnings_as_error=parser_config['warnings_as_error'])

    output = generator.generate()

    logger.info('wurfapi doxygen XML {}'.format(output))

    if 'patch_api' in parser_config:
        patch_api = parser_config['patch_api']
    else:
        patch_api = []

    # Get project root
    if 'project_root' in app.config.wurfapi:
        project_root = app.config.wurfapi['project_root']
    else:
        project_root = str(run.run(
            command='git rev-parse --show-toplevel', cwd=app.srcdir).stdout).strip()

    if 'include_paths' in app.config.wurfapi:
        include_paths = app.config.wurfapi['include_paths']

        # These are specified relative to the conf.py
        include_paths = [os.path.join(app.srcdir, p) for p in include_paths]

    else:
        include_paths = []

    # Location mapper
    mapper = location_mapper.LocationMapper(
        project_root=project_root, include_paths=include_paths, log=logger)

    parser = doxygen_parser.DoxygenParser(
        doxygen_path=output,
        location_mapper=mapper,
        patch_api=patch_api,
        log=logger)

    api = parser.parse_index()

    if 'collapse_inline_namespaces' in parser_config:
        selectors = parser_config['collapse_inline_namespaces']
    else:
        selectors = []

    api = collapse_inline_namespaces.collapse_inline_namespaces(
        api=api, selectors=selectors)

    # Instatiate the link provider
    provider = link_provider.LinkProvider(user_mappings=[])

    # Try to find additonal links across the API - making it possible for the
    # user to jump more conveniently around in the docs
    mapper = link_mapper.LinkMapper(api=api, link_provider=provider)
    api = mapper.map()

    # Dump the API
    with open(os.path.join(app.doctreedir, 'wurfapi_api.json'), 'w') as f:
        json.dump(api, f, indent=4, sort_keys=True)

    # Run schema checks on the API
    check_api_schema.check_api_schema(api=api)

    # Store the final API
    app.wurfapi_api = api


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
    app.add_directive(name='wurfapi', cls=WurfapiDirective)

    # Generate the XML
    app.connect(event="builder-inited", callback=generate_doxygen)

    # We use the doctreedir as build directory. The default for this
    # is inside _build/.doctree folder
    build_dir = os.path.join(app.doctreedir, 'wurfapi')

    # Run Doxygen on the source code

    return {'version': VERSION}
