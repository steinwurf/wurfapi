import os
import re


def transform_keys(data, key, function):
    """ Runs the function on all values with the specified key

    :param data: The dict containing the keys
    :param key: The key to look for
    :param function: The function to apply to the key's value
    """

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                data[k] = function(v)

            transform_keys(v, key, function)

    if isinstance(data, list):

        for v in data:
            transform_keys(v, key, function)


# Keywords used to split a C++ type into it's basic elements:
#
#
keywords = ["<", ">", ")", "(", "&", "*", ",", "const", "constexpr"]
keyword_pattern = '(' + '|'.join([re.escape(k) for k in keywords]) + ')'
whitespace_pattern = "(^[ \t]|[ \t]$)"


def split_cpptype(cpptype):
    """ Split a C++ type into it's basic string components.

    Example:

        Given: "const std::function<void(uint32_t*, long double)>&"

        We want a list consiting of the following strings:

        result = ["const", " ", "std::function", "<", "void", "(",
                    "uint32_t", ",", " ", "long double", ")", ">", "&"]

        This will allow us to match the basic types to generate links


    By joining the strings the original type should be returned.

    :param cpptype: The C++ type to split
    """

    # Split based on keywords
    items = [res for res in re.split(keyword_pattern, cpptype) if res]

    # Build the final result
    result = []

    # Make sure we preseve white space
    for item in items:
        result += [res for res in re.split(whitespace_pattern, item) if res]

    return result

# Basically we want to create links to both internal and external docs
# for the internal docs we may see a type but we need to know the scope where
# the type was seen to look in our i


class LinkMapper(object):

    def __init__(self, user_links):
        """
        """

    def map(self, api):

        transform_keys(api, "type", self._map_type)

    def _map_type(self, t):
        t["value"] = 3

        return t


def test_key():

    d = {'ok': [{'dfs': {'type': {'value': 2}}}],
         'sdf': {"type": {"value": 4}}}

    mapper = LinkMapper(user_links=None)
    mapper.map(d)

    print(d)

    expected = {'ok': [{'dfs': {'type': {'value': 3}}}],
                'sdf': {"type": {"value": 3}}}

    assert d == expected


def test_split_cpptype():

    cpptype = "const std::function<void(uint32_t*, long double)>&"

    result = split_cpptype(cpptype)

    expected = ["const", " ", "std::function", "<", "void", "(", "uint32_t", "*"
                ",", " ", "long double", ")", ">", "&"]

    assert result == expected

    cpptype = "std::vector<unsigned long long int>&&"

    result = split_cpptype(cpptype)

    expected = ["std::vector", "<", "unsigned long long int", ">", "&", "&"]

    assert result == expected
