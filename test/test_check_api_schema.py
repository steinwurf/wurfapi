import wurfapi.check_api_schema

test_api = {
    'namespace_dfsd': {
        'kind': 'namespace',
        'name': "dfsf",
        'scope': None,
        'members': ['class_dfdsfsd'],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ]
    },
    'class_dfdsfsd': {
        'kind': 'class',
        'name': 'sdfsdfsd',
        'is_template': True,
        'location': {'file': 'some.h', 'line-start': 10, 'line-end': 11},
        'scope': "fdsfd",
        'access': 'private',
        'members': ["variable_fsdfsddsfsdfs"],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'detaileddescription': [
            {'kind': 'code', 'content': 'bla bla', 'is_block': True},
            {'kind': 'list', 'ordered': True, 'items': [[
                {'kind': 'code', 'content': 'bla bla', 'is_block': True},
                {'kind': 'text', 'content': 'bla bla', 'link': None},
                {'kind': 'list', 'ordered': True, 'items': [[
                    {'kind': 'code', 'content': 'bla', 'is_block': True},
                    {'kind': 'text', 'content': 'bla', 'link': None}]]
                 }]]
             }
        ]
    },
    'enum_dfsdd': {
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
    'using_tryrt': {
        'kind': 'using',
        'name': "dfsfdsfds",
        'location': {'file': 'some.h', 'line-start': 10, 'line-end': None},
        'scope': 'dfsds',
        'access': 'private',
        'type': [{
            'value': 'uint32_t', 'link': {
                'url': False, 'value': 'function_fsdfsdfs'
            }
        }],
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ]
    },
    'function_fsdfsdfs': {
        'kind': 'function',
        'name': "dfsfdsfddfsdfs",
        'location': {'file': 'sdd.h', 'line-start': 10, 'line-end': 15},
        'scope': 'dfsds::ds',
        'return': {
            'type': [{
                'value': 'uint32_t', 'link': {
                    'url': True, 'value': 'www.steinwurf.com'
                }
            }],
            'description': [
                {'kind': 'text', 'content': 'bla bla', 'link': None}
            ]
        },
        'signature': 'void some(int a)',
        'is_template': True,
        'is_const': True,
        'is_static': False,
        'is_virtual': True,
        'is_explicit': False,
        'is_inline': True,
        'is_constructor': False,
        'is_destructor': True,
        'access': 'public',
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'parameters': [{
            'type': [{
                'value': 'uint32_t', 'link': {
                    'url': True, 'value': 'www.steinwurf.com'
                }
            }],
            'name': 'aaa',
            'description': [
                {'kind': 'text', 'content': 'bla bla', 'link': None}
            ]
        }],
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
        'location': {'file': 'sdd.h', 'line-start': 10, 'line-end': 15},
        'is_static': False,
        'is_mutable': True,
        'is_volatile': False,
        'is_const': True,
        'is_constexpr': True,
        'scope': 'dfsds::ds',
        'access': 'public',
        'briefdescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ],
        'detaileddescription': [
            {'kind': 'text', 'content': 'bla bla', 'link': None}
        ]
    },
}


def test_check_schema():

    wurfapi.check_api_schema.check_api_schema(api=test_api)
