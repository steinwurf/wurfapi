import json
import wurfapi.check_api_schema

test_api = {
    'namespace_dfsd': {
        'kind': 'namespace',
        'name': "dfsf",
        'scope': None,
        'inline': True,
        'members': ['class_dfdsfsd'],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ]
    },
    'file_dfsd': {
        'kind': 'file',
        'name': "dfsf",
        'path': "/bla/bla/file.exe"
    },
    'class_dfdsfsd': {
        'kind': 'class',
        'name': 'sdfsdfsd',
        'template_parameters': [{
            'type': [{
                'value': 'class'
            }],
            'name': "H",
            "default": [{
                'value': 'uint32_t'
            }]
        }],
        'location': {'path': 'some.h', 'line-start': 10, 'line-end': 11},
        'scope': "fdsfd",
        'access': 'private',
        'members': ["variable_fsdfsddsfsdfs"],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'code', 'content': 'bla bla', 'is_block': True},
            {'kind': 'list', 'ordered': True, 'items': [[
                {'kind': 'code', 'content': 'bla bla', 'is_block': True},
                {'kind': 'text', 'content': 'bla bla'},
                {'kind': 'list', 'ordered': True, 'items': [[
                    {'kind': 'code', 'content': 'bla', 'is_block': True},
                    {'kind': 'text', 'content': 'bla'}]]
                 }]]
             }
        ]
    },
    'enum_dfsdd': {
        'kind': 'enum',
        'name': "dfsfdsfds",
        'location': {
            'path': 'some.h',
            'include': 'some.h',
            'line-start': 10,
            'line-end': None
        },
        'scope': None,
        'access': 'public',
        'values': [
            {
                'name': 'a',
                'briefdescription': [
                    {'kind': 'text', 'content': 'bla bla'}
                ],
                'detaileddescription': [
                    {'kind': 'text', 'content': 'bla bla'}
                ],
                'value': "dsf"
            },
            {
                'name': 'b',
                'briefdescription': [
                    {'kind': 'text', 'content': 'bla bla'}
                ],
                'detaileddescription': [
                    {'kind': 'text', 'content': 'bla bla'}
                ]
            }
        ],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ]
    },
    'using_tryrt': {
        'kind': 'using',
        'name': "dfsfdsfds",
        'location': {'path': 'some.h', 'line-start': 10, 'line-end': None},
        'scope': 'dfsds',
        'access': 'private',
        'type': [{
            'value': 'uint32_t', 'link': {
                'url': False, 'value': 'function_fsdfsdfs'
            }
        }],
        'briefdescription': [
            {
                'kind': 'text', 'content': 'bla bla', 'link': {
                    'url': True, 'value': 'www.steinwurf.com'
                }
            }
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ]
    },
    'function_fsdfsdfs': {
        'kind': 'function',
        'name': "dfsfdsfddfsdfs",
        'location': {'path': 'sdd.h', 'line-start': 10, 'line-end': 15},
        'scope': 'dfsds::ds',
        'return': {
            'type': [{
                'value': 'uint32_t', 'link': {
                    'url': True, 'value': 'www.steinwurf.com'
                }
            }],
            'description': [
                {'kind': 'text', 'content': 'bla bla'}
            ]
        },
        'is_const': True,
        'is_static': False,
        'is_virtual': True,
        'is_explicit': False,
        'is_inline': True,
        'is_constructor': False,
        'is_destructor': True,
        'access': 'public',
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'parameters': [
            {
                'type': [{
                    'value': 'uint32_t', 'link': {
                        'url': True, 'value': 'www.steinwurf.com'
                    }
                }],
                'name': 'aaa',
                'description': [
                    {'kind': 'text', 'content': 'bla bla'}
                ]
            },
            {
                'type': [{'value': 'uint32_t'}],
                'description': [
                    {'kind': 'text', 'content': 'bla bla'}
                ]
            }
        ],
    },
    'function_fsdfsdfsaa': {
        'kind': 'function',
        'name': "dfsfdsfddfsdfs",
        'location': {'path': 'sdd.h', 'line-start': 10, 'line-end': 15},
        'scope': 'dfsds::ds',
        'is_const': True,
        'is_static': False,
        'is_virtual': True,
        'is_explicit': False,
        'is_inline': True,
        'is_constructor': False,
        'is_destructor': True,
        'access': 'public',
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'parameters': []
    },
    'variable_fsdfsddsfsdfs': {
        'kind': 'variable',
        'name': "dfsfdsfddfsdfs",
        'value': '10',
        'type': [{
            'value': 'uint32_t', 'link': {
                'url': True, 'value': 'www.steinwurf.com'
            }
        }],
        'location': {'path': 'sdd.h', 'line-start': 10, 'line-end': 15},
        'is_static': False,
        'is_mutable': True,
        'is_volatile': False,
        'is_const': True,
        'is_constexpr': True,
        'scope': 'dfsds::ds',
        'access': 'public',
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla'}
        ]
    },
}


def test_check_schema():

    wurfapi.check_api_schema.check_api_schema(api=test_api)


# def test_check_custom_schema():

#     with open('/tmp/giit/data/build/stub-5d6b38/docs/update-docs/.doctrees/wurfapi_api.json') as f:
#         test_api2 = json.load(f)

#     reduced = {
#         "stub::function<R(Args...)>": {
#             "access": "public",
#             "briefdescription": [
#             ],
#             "detaileddescription": [
#                 {
#                     "content": "return_handler.hpp",
#                     "kind": "text",
#                     "link": {
#                         "url": False,
#                         "value": "return__handler_8hpp_source"
#                     }
#                 }
#             ],
#             "kind": "class",
#             "location": {
#                 "include": "stub/function.hpp",
#                 "line-end": 258,
#                 "line-start": 67,
#                 "path": "src/stub/function.hpp"
#             },
#             "members": [
#             ],
#             "name": "function< R(Args...)>",
#             "scope": "stub",
#         }
#     }

#     wurfapi.check_api_schema.check_api_schema(api=reduced)
