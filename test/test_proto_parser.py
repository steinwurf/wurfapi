import pathlib
import re

import tree_sitter_proto
import tree_sitter


class ParserFunction:
    def __init__(self, function, type):
        self.function = function
        self.type = type


class ProtoParser:

    default_parsers = []

    def __init__(self, proto_dir, log):

        # Get the proto directory
        self.proto_dir = pathlib.Path(proto_dir)

        # Get all the proto files in the directory
        self.proto_files = self.proto_dir.glob("*.proto")

        self.log = log

        # The current scope (this is used to create an unique name for each
        # message, enum, etc.)
        self.scope = []

        # The top level API
        self.api = {}

    def push_scope(self, scope):
        self.scope.append(scope)

    def pop_scope(self):
        self.scope.pop()

    def get_scope(self):
        return ".".join(self.scope)

    def add_top_level(self, unique_name, entity):
        """Add a top level entity to the API"""

        assert unique_name not in self.api
        self.api[unique_name] = entity

    def parse(self):

        for proto_file in self.proto_files:

            # Read as bytes
            with open(proto_file, "rb") as f:
                proto_content = f.read()

            language = tree_sitter.Language(tree_sitter_proto.language())

            parser = tree_sitter.Parser(language)

            tree = parser.parse(proto_content)

            api = self.parse_node(node=tree.root_node)

        assert False

    def parse_node(self, node):
        """Parse a node in the AST"""

        # Find the parser function for this type
        parser = None
        for p in self.default_parsers:
            if p.type == node.type:
                parser = p.function
                break

        if parser is None:
            raise ValueError(f"No parser found for type {node.type}")

        return parser(parser=self, node=node, log=self.log)

    @staticmethod
    def register(type):
        """Decorator for registering a parser function for a specific type"""

        def _register(function):

            for parser in ProtoParser.default_parsers:
                if parser.type == type:
                    raise ValueError(f"Parser for type {type} already exists")

            ProtoParser.default_parsers.append(ParserFunction(function, type))
            return function

        return _register


def child_by_node_type(node, type):
    for child in node.children:
        if child.type == type:
            return child

    raise ValueError(f"Field type {type} not found in node {node} children")


def has_child_by_node_type(node, type):
    try:
        node = child_by_node_type(node, type)
        return True
    except ValueError:
        return False


@ProtoParser.register("syntax")
def parse(parser, node, log):
    return {}


@ProtoParser.register("package")
def parse(parser, node, log):

    # In the parse tree, the package is a full_ident
    # (package (full_ident (identifier) (identifier)))
    # Let use a query to get the package name

    package = child_by_node_type(node, "full_ident").text.decode()

    result = {}
    result["kind"] = "package"
    result["name"] = package

    unique_name = package

    parser.push_scope(package)
    parser.add_top_level(unique_name, result)

    return {}


@ProtoParser.register("option")
@ProtoParser.register("field_option")
def parse(parser, node, log):
    value = {}

    name_node = node.child_by_field_name("name")
    value_node = node.child_by_field_name("value")

    value["name"] = name_node.text.decode()
    value["value"] = value_node.text.decode()
    value["kind"] = "option"

    # Option names may have "open parenthesis" and "close parenthesis"
    # Example:
    #   int32 rounds = 6 [ (description) = "The number of rounds" ];
    #
    # We strip the parenthesis if they are present
    if value["name"].startswith("(") and value["name"].endswith(")"):
        value["name"] = value["name"][1:-1]

    return value


@ProtoParser.register("field_options")
def parse(parser, node, log):

    options = []

    for child in node.children:
        if child.type == "field_option":
            options.append(parser.parse_node(child))

    return options


@ProtoParser.register("enum")
def parse(parser, node, log):

    # Get enum (find enum_name type)
    name = child_by_node_type(node, "enum_name").text.decode()

    result = {}
    result["kind"] = "enum"
    result["name"] = name
    result["scope"] = parser.get_scope()

    body = child_by_node_type(node, "enum_body")

    values = []
    for child in body.children:
        if child.type == "enum_field":

            # Check for comment before or after the field
            comment = None

            if child.prev_sibling is not None:
                if child.prev_sibling.type == "comment":
                    comment = child.prev_sibling.text.decode()

            if child.next_sibling is not None:
                if child.next_sibling.type == "comment":
                    comment = child.next_sibling.text.decode()

            value = {}
            value["name"] = child_by_node_type(child, "enum_variant_name").text.decode()
            value["id"] = child_by_node_type(child, "field_number").text.decode()

            if comment is not None:
                value["comment"] = comment

            values.append(value)

    result["values"] = values

    unique_name = parser.get_scope() + "." + name

    parser.add_top_level(unique_name, result)

    return unique_name


@ProtoParser.register("oneof_field")
@ProtoParser.register("field")
def parse(parser, node, log):

    # Check for comment before or after the field
    comment = None

    if node.prev_sibling is not None:
        if node.prev_sibling.type == "comment":
            comment = node.prev_sibling.text.decode()

    if node.next_sibling is not None:
        if node.next_sibling.type == "comment":
            comment = node.next_sibling.text.decode()

    member = {}

    member["name"] = child_by_node_type(node, "field_name").text.decode()
    member["type"] = child_by_node_type(node, "type").text.decode()
    member["id"] = child_by_node_type(node, "field_number").text.decode()

    if node.type == "field":
        # Does not make sense for oneof fields
        member["is_repeated"] = has_child_by_node_type(node, "repeated")
        member["is_optional"] = has_child_by_node_type(node, "optional")

    if comment is not None:
        member["comment"] = comment

    if has_child_by_node_type(node, "field_options"):
        member["options"] = parser.parse_node(child_by_node_type(node, "field_options"))

    return member


@ProtoParser.register("oneof")
def parse(parser, node, log):

    # Get oneof (find oneof_name type)
    name = child_by_node_type(node, "identifier").text.decode()

    result = {}
    result["kind"] = "oneof"
    result["name"] = name
    result["scope"] = parser.get_scope()

    body = child_by_node_type(node, "oneof_body")

    members = []
    for child in body.named_children:
        if child.type == "oneof_field":
            members.append(parser.parse_node(child))

    result["members"] = members

    return result


@ProtoParser.register("message")
def parse(parser, node, log):

    # Get message (find message_name type)
    name = child_by_node_type(node, "message_name").text.decode()

    result = {}
    result["kind"] = "message"
    result["name"] = name
    result["scope"] = parser.get_scope()

    body = child_by_node_type(node, "message_body")

    parser.push_scope(name)

    result["members"] = []
    for child in body.named_children:

        if child.type == None:
            continue

        result["members"].append(parser.parse_node(child))

    parser.pop_scope()

    unique_name = parser.get_scope() + "." + name

    parser.add_top_level(unique_name, result)

    return unique_name


@ProtoParser.register("source_file")
def parse(parser, node, log):
    print("Parsing source file")
    print(node)

    print(type(parser))

    result = {}
    result["kind"] = "source_file"
    result["name"] = "source_file"

    for child in node.children:

        if child.type == "syntax":
            result["syntax"] = parser.parse_node(child)

        if child.type == "package":
            result["package"] = parser.parse_node(child)

        if child.type == "option":

            if "options" not in result:
                result["options"] = []

            result["options"].append(parser.parse_node(child))

        if child.type == "message":
            result["message"] = parser.parse_node(child)

    ##for child in node.children:
    #    api.update(parser.parse_node(child))

    parser.api = result

    print(parser.api)

    assert False


def test_proto_parse(testdirectory):

    log = None

    proto_dir = testdirectory.copy_dir("test/data/proto")

    parser = ProtoParser(proto_dir=proto_dir.path(), log=log)
    parser.parse()
    # caplog.set_level(logging.DEBUG)

    # coffee_dir, src_dirs, xml_dir = generate_coffee_xml(testdirectory)
    # log = logging.getLogger(name="test_coffee")

    # mapper = wurfapi.location_mapper.LocationMapper(
    #     project_root=coffee_dir, include_paths=[], log=log
    # )

    # parser = wurfapi.doxygen_parser.DoxygenParser(
    #     doxygen_path=xml_dir,
    #     location_mapper=mapper,
    #     # Patch fix Doxygen bug reported here:
    #     # https://bit.ly/2BWPllZ
    #     patch_api=[
    #         {
    #             "selector": "project::v1_0_0::coffee::machine::impl",
    #             "key": "access",
    #             "value": "private",
    #         }
    #     ],
    #     log=log,
    # )

    # api_data = parser.parse_index()

    # datarecorder.record_data(
    #     data=api_data,
    #     recording_file="test/data/parser_recordings/coffee.json",
    # )
