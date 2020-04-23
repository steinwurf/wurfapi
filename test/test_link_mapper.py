import functools
import mock
import wurfapi.link_mapper


def test_transform_key():

    data = [{'taco': 42}, {'salsa': [{'burrito': {'taco': 69}}]}]

    def map_taco(value, scope):
        return value * 2

    wurfapi.link_mapper.transform_key(
        data=data, search_key='taco', scope=None, function=map_taco)

    expected = [{'taco': 84}, {'salsa': [{'burrito': {'taco': 138}}]}]

    assert data == expected


def test_split_cpptype():

    cpptype = "const std::function<void(uint32_t*, long double)>&"

    result = wurfapi.link_mapper.split_cpptype(cpptype)

    expected = ["const", " ", "std::function", "<", "void", "(", "uint32_t",
                "*", ",", " ", "long double", ")", ">", "&"]

    assert result == expected

    cpptype = "std::vector<unsigned long long int>&&"

    result = wurfapi.link_mapper.split_cpptype(cpptype)

    expected = ["std::vector", "<", "unsigned long long int", ">", "&", "&"]

    assert result == expected


def test_split_typelist():

    typelist = [{"value": "const "},
                {"value": "std::function", "link": {
                    'url': True, 'value': 'www.isocpp.org'}},
                {"value": "<void(uint32_t*, long double)>&"}]

    result = wurfapi.link_mapper.split_typelist(typelist=typelist)

    print(result)

    expected = [{'value': 'const'},
                {'value': ' '},
                {'link': {'url': True, 'value': 'www.isocpp.org'},
                    'value': 'std::function'},
                {'value': '<'},
                {'value': 'void'},
                {'value': '('},
                {'value': 'uint32_t'},
                {'value': '*'},
                {'value': ','},
                {'value': ' '},
                {'value': 'long double'},
                {'value': ')'},
                {'value': '>'},
                {'value': '&'}]

    assert result == expected


def test_join_typelist():

    typelist = [{'value': 'const'},
                {'value': ' '},
                {'link': {'url': True, 'value': 'www.isocpp.org'},
                    'value': 'std::function'},
                {'value': '<'},
                {'value': 'void'},
                {'value': '('},
                {'value': 'uint32_t'},
                {'value': '*'},
                {'value': ','},
                {'value': ' '},
                {'value': 'long double'},
                {'value': ')'},
                {'value': '>'},
                {'value': '&'}]

    result = wurfapi.link_mapper.join_typelist(typelist=typelist)

    expected = [{"value": "const "},
                {"value": "std::function", "link": {
                    'url': True, 'value': 'www.isocpp.org'}},
                {"value": "<void(uint32_t*, long double)>&"}]

    print(result)

    assert result == expected


def test_linkmapper():

    api = {'object': {'type': [
        {'value': 'const std::function<void(uint32_t*, long double)>&'}]}, 'uint32_t': "dummy"}

    provider = mock.Mock()
    provider.find_link.return_value = None

    mapper = wurfapi.link_mapper.LinkMapper(api=api, link_provider=provider)

    result = mapper.map()

    print(result)

    expected = {'object':
                {'type': [
                    {'value': 'const std::function<void('},
                    {'link': {"url": False, "value": 'uint32_t'}, 'value': 'uint32_t'},
                    {'value': '*, long double)>&'}]},
                'uint32_t': 'dummy'}

    assert result == expected


def test_split_cppscope():

    cppscope = "std::function"

    result = wurfapi.link_mapper.split_cppscope(cppscope)

    expected = ["std::function", "std"]

    assert result == expected

    cppscope = "std"

    result = wurfapi.link_mapper.split_cppscope(cppscope)

    expected = ["std"]

    assert result == expected

    cppscope = None

    result = wurfapi.link_mapper.split_cppscope(cppscope)

    expected = []

    assert result == expected


def test_split_text():

    text = {'content': "some list of words", "kind": "text"}

    result = wurfapi.link_mapper.split_text(text=text)

    expected = [
        {'content': 'some', 'kind': 'text'},
        {'content': 'list', 'kind': 'text'},
        {'content': 'of', 'kind': 'text'},
        {'content': 'words', 'kind': 'text'}
    ]

    assert result == expected


# def test_split_paragraphs():

#     paragraphs = [
#         [
#             {'kind': 'code'},
#             {'kind': 'text', 'content': 'some list of words'},
#             {'kind': 'list', 'items': [[
#                 [{'content': 'some words', 'kind': 'text'}]
#             ]]}
#         ]
#     ]

#     result = wurfapi.link_mapper.split_paragraphs(paragraphs=paragraphs)

#     expected = [
#         {'kind': 'code'},
#         {'content': 'some', 'kind': 'text'},
#         {'content': 'list', 'kind': 'text'},
#         {'content': 'of', 'kind': 'text'},
#         {'content': 'words', 'kind': 'text'},
#         {'kind': 'list',
#         'items': [[
#             {'content': 'some', 'kind': 'text'},
#             {'content': 'words', 'kind': 'text'}
#         ]]}
#     ]

#     assert result == expected


# def test_join_paragraphs():

#     paragraphs = [
#         {'kind': 'code'},
#         {'content': 'some', 'kind': 'text'},
#         {'content': 'list', 'kind': 'text'},
#         {'content': 'of', 'kind': 'text'},
#         {'content': 'words', 'kind': 'text'},
#         {'kind': 'list',
#          'items': [[
#              {'content': 'some', 'kind': 'text'},
#              {'content': 'words', 'kind': 'text'}
#          ]]
#          }
#     ]

#     result = wurfapi.link_mapper.join_paragraphs(paragraphs=paragraphs)

#     expected = [
#         {'kind': 'code'},
#         {'content': 'some list of words', 'kind': 'text'},
#         {'kind': 'list', 'items': [[
#             {'content': 'some words', 'kind': 'text'}
#         ]]}
#     ]

#     assert result == expected
