import os


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
