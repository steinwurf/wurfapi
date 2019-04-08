import os
import re
import copy


def transform_key(data, search_key, scope, function):
    """ Runs the function on all values with the specified key

    :param data: The dict containing the keys
    :param key: The key to look for
    :param scope: The current scope where the type has been seen
    :param function: The function to apply to the key's value
    """

    if isinstance(data, dict):

        if 'scope' in data:
            scope = data['scope']

        for found_key, value in data.items():

            if found_key == 'scope':
                continue

            if found_key == search_key:
                data[found_key] = function(value=value, scope=scope)

            transform_key(data=value, search_key=search_key,
                          scope=scope, function=function)

    if isinstance(data, list):

        for value in data:
            transform_key(data=value, search_key=search_key,
                          scope=scope, function=function)


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

    :param cpptype: The C++ type to split as a string
    :return: A list of tokens and basic components.
    """

    # Split based on keywords
    items = [res for res in re.split(keyword_pattern, cpptype) if res]

    # Build the final result
    result = []

    # Make sure we preseve white space
    for item in items:
        result += [res for res in re.split(whitespace_pattern, item) if res]

    return result


def split_typelist(typelist):
    """ Splits a type list into as small compoenets as possible

    :param typelist: A wurfapi type list.
    :return: An expanded wurfapi type list.
    """

    newlist = []

    for item in typelist:

        if item["link"] is not None:

            # We already have a link for this item of the type
            newlist.append(item)
            continue

        # See if we can split the element out in more components
        # e.g. 'std::vector<uint8_t>' gets split into 'std::vector', '<',
        # 'uint8_t', '>'
        tokens = split_cpptype(cpptype=item['value'])

        for token in tokens:
            newlist.append({"value": token, "link": None})

    return newlist


def join_typelist(typelist):
    """ Takes a type list and joins it into as few components as possible

    :param typelist: A wurfapi type list.
    :return: An reduced wurfapi type list.
    """

    newlist = []

    temporary_item = {'value': "", "link": None}

    for item in typelist:

        # We have the following cases:

        # 2. We just get a new item with a link
        # 3. The new item does not have a link

        if item["link"] and temporary_item["value"]:
            # We got an item with a link and we have already accumulated
            # something in the temporary_item
            newlist.append(temporary_item)
            temporary_item = {'value': "", "link": None}

        if item["link"]:
            newlist.append(item)
        else:
            temporary_item["value"] += item["value"]

    if temporary_item["value"]:
        newlist.append(temporary_item)

    return newlist


def split_cppscope(cppscope):
    """ Split a C++ sceop into a list of more an more general scopes.

    Example:

        The scope "foo::bar::example" should be transformed to a list
        such as:

            scopes = ["foo::bar::example", "foo::bar", "foo"]

    :param cppscope: The C++ scope as a string
    :return: A list of C++ scopes of decreasing locality
    """

    scopes = []

    while cppscope:
        scopes.append(cppscope)
        cppscope, _, _ = cppscope.rpartition('::')

    return scopes


class LinkMapper(object):

    def __init__(self, api):
        """ Create a new instance

        :param api: The API to map
        """
        self.api = api

    def map(self):
        """ Perform the actual mapping.

        :return: A modified API with links expanced. The original API dict is
            not modified.
        """

        mapped_api = copy.deepcopy(self.api)

        transform_key(data=mapped_api, search_key="type", scope=None,
                      function=self._map_type)

        return mapped_api

    def _map_type(self, value, scope):
        """ Find links in the 'type' lists """

        # 1. Split the type into it most basic elements
        typelist = split_typelist(typelist=value)

        # 2. Check if we have a link for each of the itms
        for item in typelist:

            if item['link']:
                continue

            item['link'] = self._find_link(typename=item['value'], scope=scope)

        # 3. Reduce the typelist such that only elements with links are
        #    kept standalone
        typelist = join_typelist(typelist=typelist)

        return typelist

    def _find_link(self, typename, scope):
        """ Given a token e.g. std::function see if we can find a link

        First we check if the type name is found directly in the API. After
        this we try to see if the

        :param typename: A C++ type name as a string
        :param scope: The scope
        """
        if typename in keywords:
            # Not a typename just a C++ token
            return

        if typename in self.api:
            # The typename was found diretly in the API
            return typename

        if scope is None:
            # We do not have a scope so there is nothing more we can do
            return None

        scopes = split_cppscope(cppscope=scope)

        for scope in scopes:

            scoped_name = scope + '::' + typename

            if scoped_name in self.api:
                # The scope qualified name was found
                return scoped_name

        # We give up
        return None
