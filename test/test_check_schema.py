import schema
import six

# # These are useful when defining defaults in the schema
#     default_branches = {'regex': {'filters': []},
#                         'source_branch': False}
#     default_tags = {
#         'regex': {'filters': []},
#         'semver': {'filters': [], 'relaxed': False}
#     }

#     config_schema = schema.Schema({
#         'scripts': list,
#         schema.Optional('variables', default={}): dict,
#         schema.Optional('requirements', default=None): six.text_type,
#         schema.Optional('cwd', default=os.getcwd()): six.text_type,
#         schema.Optional('python_path', default=None): six.text_type,
#         schema.Optional('branches', default=default_branches): {
#             schema.Optional("regex", default=default_branches["regex"]): {"filters": list},
#             schema.Optional("source_branch", default=default_branches["source_branch"]): bool},
#         schema.Optional('workingtree', default=False): bool,
#         schema.Optional('allow_failure', default=False): bool,
#         schema.Optional('no_git', default=False): bool,
#         schema.Optional('pip_packages', default=None): list,
#         schema.Optional('tags', default=default_tags): {
#             schema.Optional("regex", default=default_tags["regex"]): {
#                 "filters": list
#             },
#             schema.Optional("semver", default=default_tags["semver"]): {
#                 "filters": list,
#                 schema.Optional(
#                     "relaxed", default=default_tags["semver"]["relaxed"]): bool
#             }
#         }
#     })

#     config = config_schema.validate(config)


def test_check_schema():

    # Schema for checing we have a string in a Python 2 and 3 compatible way
    string_schema = schema.Schema(schema.Or(*six.string_types))

    # Schema for the members key
    members_schema = schema.Schema([string_schema])

    # Schema for checking the location
    location_schema = schema.Schema({
        'file': string_schema,
        'line-start': int,
        'line-end': schema.Or(int, None)
    })

    # Link schema
    link_schema = schema.Schema({
        'url': bool,
        'value': string_schema,
    })

    # Paragraphs text schema
    paragraphs_text_schema = schema.Schema({
        'kind': 'text',
        'content': string_schema,
        'link': schema.Or(link_schema, None)
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
        'items': items_paragraphs
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

    # Schema for checking the namespace kind
    namespace_schema = schema.Schema({
        'kind': 'namespace',
        'name': string_schema,
        'scope': schema.Or(string_schema, None),
        'members': members_schema
    })

    # Schema for checking classes and structs
    class_struct_schema = schema.Schema({
        'kind': schema.Or('class', 'struct'),
        'name': string_schema,
        'location': location_schema,
        'scope': schema.Or(string_schema, None),
        'members': members_schema,
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema
    })

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
            'value': schema.Or(string_schema, None)
        }],
        'briefdescription': paragraphs_schema,
        'detaileddescription': paragraphs_schema
    })

    # Enum schema

    api = {
        'dfsd': {
            'kind': 'namespace',
            'name': "dfsf",
            'scope': None,
            'members': []
        },
        'dfdsfsd': {
            'kind': 'class',
            'name': 'sdfsdfsd',
            'location': {'file': 'some.h', 'line-start': 10, 'line-end': 11},
            'scope': "fdsfd",
            'members': ["sdfds"],
            'briefdescription': [
                {'kind': 'text', 'content': 'bla bla', 'link': None}
            ],
            'detaileddescription': [
                {'kind': 'code', 'content': 'bla bla', 'is_block': True},
                {'kind': 'list', 'ordered': True, 'items': [
                    {'kind': 'code', 'content': 'bla bla', 'is_block': True},
                    {'kind': 'text', 'content': 'bla bla', 'link': None},
                    {'kind': 'list', 'ordered': True, 'items': [
                        {'kind': 'code', 'content': 'bla', 'is_block': True},
                        {'kind': 'text', 'content': 'bla', 'link': None}]
                     }]
                 }
            ]
        },
        'dfsd': {
            'kind': 'enum',
            'name': "dfsfdsfds",
            'location': {'file': 'some.h', 'line-start': 10, 'line-end': None},
            'scope': None,
            'access': 'public',
            'values': [{
                'name': 'a',
                'briefdescription': [
                    {'kind': 'text', 'content': 'bla bla', 'link': None}
                ],
                'detaileddescription': [
                    {'kind': 'text', 'content': 'bla bla', 'link': None}
                ],
                'value': None
            }],
            'briefdescription': [
                {'kind': 'text', 'content': 'bla bla', 'link': None}
            ],
            'detaileddescription': [
                {'kind': 'text', 'content': 'bla bla', 'link': None}
            ]
        },
    }

    api_schema = schema.Schema({
        str: schema.Or(
            namespace_schema,
            class_struct_schema,
            enum_schema
        )
    })

    api = api_schema.validate(api)
