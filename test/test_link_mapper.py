import wurfapi.link_mapper


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

    typelist = [{"value": "const ", "link": None},
                {"value": "std::function", "link": "www.isocpp.org"},
                {"value": "<void(uint32_t*, long double)>&", "link": None}]

    result = wurfapi.link_mapper.split_typelist(typelist=typelist)

    print(result)

    expected = [{'link': None, 'value': 'const'},
                {'link': None, 'value': ' '},
                {'link': 'www.isocpp.org', 'value': 'std::function'},
                {'link': None, 'value': '<'},
                {'link': None, 'value': 'void'},
                {'link': None, 'value': '('},
                {'link': None, 'value': 'uint32_t'},
                {'link': None, 'value': '*'},
                {'link': None, 'value': ','},
                {'link': None, 'value': ' '},
                {'link': None, 'value': 'long double'},
                {'link': None, 'value': ')'},
                {'link': None, 'value': '>'},
                {'link': None, 'value': '&'}]

    assert result == expected


def test_join_typelist():

    typelist = [{'link': None, 'value': 'const'},
                {'link': None, 'value': ' '},
                {'link': 'www.isocpp.org', 'value': 'std::function'},
                {'link': None, 'value': '<'},
                {'link': None, 'value': 'void'},
                {'link': None, 'value': '('},
                {'link': None, 'value': 'uint32_t'},
                {'link': None, 'value': '*'},
                {'link': None, 'value': ','},
                {'link': None, 'value': ' '},
                {'link': None, 'value': 'long double'},
                {'link': None, 'value': ')'},
                {'link': None, 'value': '>'},
                {'link': None, 'value': '&'}]

    result = wurfapi.link_mapper.join_typelist(typelist=typelist)

    expected = [{"value": "const ", "link": None},
                {"value": "std::function", "link": "www.isocpp.org"},
                {"value": "<void(uint32_t*, long double)>&", "link": None}]

    print(result)

    assert result == expected


def test_linkmapper():

    api = {'object': {'type': [
        {'value': 'const std::function<void(uint32_t*, long double)>&', 'link': None}]}, 'uint32_t': "dummy"}

    mapper = wurfapi.link_mapper.LinkMapper(api=api)

    result = mapper.map()

    print(result)

    expected = {'object': {'type': [{'link': None, 'value': 'const std::function<void('}, {'link': 'uint32_t', 'value': 'uint32_t'}, {
        'link': None, 'value': '*, long double)>&'}]}, 'uint32_t': 'dummy'}

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
