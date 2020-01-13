import os
import re
import copy
import functools


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

        if "link" in item:

            # We already have a link for this item of the type
            newlist.append(item)
            continue

        # See if we can split the element out in more components
        # e.g. 'std::vector<uint8_t>' gets split into 'std::vector', '<',
        # 'uint8_t', '>'
        tokens = split_cpptype(cpptype=item['value'])

        for token in tokens:
            newlist.append({"value": token})

    return newlist


def join_typelist(typelist):
    """ Takes a type list and joins it into as few components as possible

    :param typelist: A wurfapi type list.
    :return: An reduced wurfapi type list.
    """

    newlist = []

    temporary_item = {'value': ""}

    for item in typelist:

        # We have the following cases:

        # 1. We just get a new item with a link
        # 2. The new item does not have a link

        if "link" in item and temporary_item["value"]:
            # We got an item with a link and we have already accumulated
            # something in the temporary_item
            newlist.append(temporary_item)
            temporary_item = {'value': ""}

        if "link" in item:
            newlist.append(item)
        else:
            temporary_item["value"] += item["value"]

    if temporary_item["value"]:
        newlist.append(temporary_item)

    return newlist


def split_cppscope(cppscope):
    """ Split a C++ scope into a list of more general scopes.

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


def split_text(text):
    """ Takes a text item and splits it into a list of words.

    :return: List of text items
    """

    words = text['content'].split()

    result = []
    for word in words:
        result.append({'kind': 'text', 'content': word})

    return result


def split_paragraphs(paragraphs):
    """ Takes a list of pragraphs and splits it into as many compenents
    as possible.

    :param paragraphs: A list of paragraphs
    :return: An expanded list of paragraphs
    """

    newlist = []

    for paragraph in paragraphs:

        if paragraph['kind'] is "code":
            newlist.append(paragraph)
            continue

        if paragraph['kind'] is "list":

            items = []
            for item in paragraph['items']:
                items.append(split_paragraphs(paragraphs=item))

            paragraph['items'] = items

            newlist.append(paragraph)
            continue

        if "link" in paragraph:
            newlist.append(paragraph)
            continue

        newlist += split_text(paragraph)

    return newlist


def join_paragraphs(paragraphs):
    """ Takes a list of pragraphs and joins it into as few compenents
    as possible.

    :param paragraphs: A list of paragraphs
    :return: An recduced list of paragraphs
    """

    result = []

    # We use this item to accumulate the content from adjacent
    # text elements
    text = []

    def _flush(paragraphs, text):
        if text:
            paragraphs.append(
                {'kind': 'text', 'content': " ".join(text)})

            # Remove all elements in the list
            del text[:]

    flush = functools.partial(_flush, paragraphs=result, text=text)

    for paragraph in paragraphs:

        if paragraph['kind'] is "code":
            flush()
            result.append(paragraph)
            continue

        if paragraph['kind'] is "list":

            # A list contains even more paragraphs
            items = []

            for item in paragraph['items']:
                items.append(join_paragraphs(paragraphs=item))

            paragraph['items'] = items

            flush()
            result.append(paragraph)
            continue

        if "link" in paragraph:
            flush()
            result.append(paragraph)
            continue

        text.append(paragraph['content'])

    # If anything remains in the temporary flush it out
    flush()

    return result


class LinkMapper(object):

    def __init__(self, api, link_provider):
        """ Create a new instance

        :param api: The API to map
        :param link_provider: Helper to resolve links to more types
        """
        self.api = api
        self.link_provider = link_provider

    def map(self):
        """ Perform the actual mapping.

        :return: A modified API with links expanced. The original API dict is
            not modified.
        """

        mapped_api = copy.deepcopy(self.api)

        transform_key(data=mapped_api, search_key="type", scope=None,
                      function=self._map_type)

        transform_key(data=mapped_api, search_key="briefdescription",
                      scope=None, function=self._map_paragraphs)

        transform_key(data=mapped_api, search_key="detaileddescription",
                      scope=None, function=self._map_paragraphs)

        return mapped_api

    def _map_paragraphs(self, value, scope):
        """ Find links in the 'text' elements """

        # 1. Split all the paragraphs into

        paragraphs = split_paragraphs(paragraphs=value)

        def _add_links(paragraphs):

            for paragraph in paragraphs:

                if paragraph['kind'] is 'code':
                    continue

                if paragraph['kind'] is 'list':
                    for item in paragraph['items']:
                        _add_links(item)

                    continue

                if 'link' in paragraph:
                    continue

                if "::" not in paragraph['content']:
                    # We skip over stuff that does not have a scope
                    # qualifier in it. Just to avoid making random
                    # characters into links..
                    continue

                link = self._find_link(
                    typename=paragraph['content'], scope=scope)

                if link:
                    paragraph['link'] = link

        _add_links(paragraphs=paragraphs)

        paragraphs = join_paragraphs(paragraphs=paragraphs)

        return paragraphs

    def _map_type(self, value, scope):
        """ Find links in the 'type' lists """

        # 1. Split the type into it most basic elements
        typelist = split_typelist(typelist=value)

        # 2. Check if we have a link for each of the itms
        for item in typelist:

            if "link" in item:
                # If we do have a link to a type it should be in the API
                assert item["link"]["value"] in self.api

                continue

            link = self._find_link(typename=item['value'], scope=scope)

            if link is not None:
                item['link'] = link

        # 3. Reduce the typelist such that only elements with links are
        #    kept standalone
        typelist = join_typelist(typelist=typelist)

        return typelist

    def _find_link(self, typename, scope):
        """ Given a token e.g. std::function see if we can find a link

        First we check if the type name is found directly in the API. After
        this we try to see if the link_provider has one.

        :param typename: A C++ type name as a string
        :param scope: A scope as a string otherwise None
        """
        if typename in keywords:
            # Not a typename just a C++ token
            return

        if typename in self.api:
            # The typename was found diretly in the API
            return {"url": False, "value": typename}

        if scope is None:
            # We do not have a scope so there is nothing more we can do
            return None

        scopes = split_cppscope(cppscope=scope)

        for scope in scopes:

            scoped_name = scope + '::' + typename

            if scoped_name in self.api:
                # The scope qualified name was found
                return {"url": False, "value": scoped_name}

        # Finally try the link provider - which either returns None or a link
        return self.link_provider.find_link(typename=typename)
