import schema
import six


def check_api_schema(api):
    """ Checks the schema of the API and raises exceptions if something
    does not match.

    :param api: The API dictionary
    """

    # Schema for checking we have a string in a Python 2 and 3 compatible way

    # Link schema
    class StringSchema(object):

        def validate(self, data):

            # Check the basic properties
            schema.Schema(schema.Or(*six.string_types)).validate(data)

            # No empty strings either
            if not data:
                raise schema.SchemaError("String is empty")

            return data

    string_schema = StringSchema()

    # Schema for checking the location
    location_schema = schema.Schema({
        'path': string_schema,
        schema.Optional('include'): string_schema,
        'line-start': int,
        'line-end': schema.Or(int, None)
    })

    # Check that members's 'unique-name' is in the API
    class MemberInAPI(object):
        def __init__(self, api):
            self.api = api

        def validate(self, data):

            if data not in self.api:
                raise schema.SchemaError(
                    "%r not found in the API "
                    "valid keys are %r" % (data, self.api.keys()))

            return data

    # Link schema
    class LinkSchema(object):
        def __init__(self, api):
            self.api = api

        def validate(self, data):

            # Check the basic properties
            schema.Schema({
                'url': bool,
                'value': string_schema,
            }).validate(data)

            # For url we are done
            if data['url']:
                return data

            # Check that if non url we have the link in the API
            if data['value'] not in self.api:
                raise schema.SchemaError(
                    "Link value %r not found in the API "
                    "valid keys are %r" % (data, self.api.keys()))

            return data

    # Paragraphs text schema
    paragraphs_text_schema = schema.Schema({
        'kind': 'text',
        'content': string_schema,
        schema.Optional('link'): LinkSchema(api=api)
    })

    # Paragraphs code schema
    paragraphs_code_schema = schema.Schema({
        'kind': 'code',
        'content': string_schema,
        'is_block': bool
    })

    # Paragraphs list schema

    class ItemsParagraphs(object):

        def __init__(self):
            self.use_schema = None

        def validate(self, data):
            return self.use_schema.validate(data)

    # We define a validator object but defer the initilization of the schema to
    # use. The reason is the items kind is itself a list of paragraphs so we
    # have a recursive dependency.
    items_paragraphs = ItemsParagraphs()

    paragraphs_list_schema = schema.Schema({
        'kind': 'list',
        'ordered': bool,
        'items': [items_paragraphs]
    })

    # Paragraphs schema
    paragraphs_schema = schema.Schema([
        schema.Or(
            paragraphs_text_schema,
            paragraphs_code_schema,
            paragraphs_list_schema
        )
    ])

    # Initilize the items schema which itself is a list of paragraphs
    items_paragraphs.use_schema = paragraphs_schema

    # type schema

    type_schema = schema.Schema([{
        'value': string_schema,
        schema.Optional('link'): LinkSchema(api=api)
    }])

    # template parameter schema

    template_parameter_schema = schema.Schema([{
        'type': type_schema,
        'name': string_schema,
        schema.Optional('default'): type_schema,
        schema.Optional('description'): paragraphs_schema
    }])

    # Schema for checking the namespace kind
    namespace_schema = schema.Schema({
        'kind': 'namespace',
        'name': string_schema,
        'scope': schema.Or(string_schema, None),
        'members': [MemberInAPI(api=api)],
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema,
        'inline': bool
    })

    # Schema for checking classes and structs
    class_struct_schema = schema.Schema({
        'kind': schema.Or('class', 'struct'),
        'name': string_schema,
        'location': location_schema,
        'scope': schema.Or(string_schema, None),
        'access': schema.Or('public', 'protected', 'private'),
        schema.Optional('template_parameters'): template_parameter_schema,
        'members': [MemberInAPI(api=api)],
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema
    })

    # Enum schema
    enum_schema = schema.Schema({
        'kind': 'enum',
        'name': string_schema,
        'location': location_schema,
        'scope': schema.Or(string_schema, None),
        'access': schema.Or('public', 'protected', 'private'),
        'values': [{
            'name': string_schema,
            'briefdescription': paragraphs_schema,
            'detaileddescription': paragraphs_schema,
            schema.Optional('value'): string_schema
        }],
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema
    })

    # Type schema
    type_schema = schema.Schema([{
        'value': string_schema,
        schema.Optional('link'): LinkSchema(api=api)
    }])

    # Typedef / using schema
    typedef_using_schema = schema.Schema({
        'kind': schema.Or('typedef', 'using'),
        'name': string_schema,
        'location': location_schema,
        'scope': schema.Or(string_schema, None),
        'access': schema.Or('public', 'protected', 'private'),
        'type': type_schema,
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema
    })

    # Function schema
    function_schema = schema.Schema({
        'kind': 'function',
        'name': string_schema,
        'location': location_schema,
        'scope': schema.Or(string_schema, None),
        schema.Optional('return'): {
            'type': type_schema,
            'description': paragraphs_schema
        },
        'signature': string_schema,
        schema.Optional('template_parameters'): template_parameter_schema,
        'is_const': bool,
        'is_static': bool,
        'is_virtual': bool,
        'is_explicit': bool,
        'is_inline': bool,
        'is_constructor': bool,
        'is_destructor': bool,
        'access': schema.Or('public', 'protected', 'private'),
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema,
        'parameters': [{
            'type': type_schema,
            schema.Optional('name'): string_schema,
            'description': paragraphs_schema
        }],
    })

    # variable schema

    variable_schema = schema.Schema({
        'kind': 'variable',
        'name': string_schema,
        schema.Optional('value'): string_schema,
        'type': type_schema,
        'location': location_schema,
        'is_static': bool,
        'is_mutable': bool,
        'is_volatile': bool,
        'is_const': bool,
        'is_constexpr': bool,
        'scope': schema.Or(string_schema, None),
        'access': schema.Or('public', 'protected', 'private'),
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema,
    })

    # Dispatch to the "right" kind of schema. We could do this with a
    # schema.Or(...) clause but it makes the error output hard to read
    api_schemas = {
        'namespace': namespace_schema,
        'class': class_struct_schema,
        'struct': class_struct_schema,
        'enum': enum_schema,
        'typedef': typedef_using_schema,
        'using': typedef_using_schema,
        'function': function_schema,
        'variable': variable_schema
    }

    class SchemaApi(object):

        def validate(self, data):

            if 'kind' not in data:
                raise schema.SchemaError(
                    "Required 'kind' key not found in %r" % data)

            if data['kind'] not in api_schemas:
                raise schema.SchemaError(
                    "Unknown 'kind' key in %r valid kinds are %r"
                    % (data, api_schemas.keys()))

            return api_schemas[data['kind']].validate(data)

    schema.Schema({
        str: SchemaApi()}).validate(api)
