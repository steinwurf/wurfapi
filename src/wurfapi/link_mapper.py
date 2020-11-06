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
                data[found_key] = function(value, scope=scope)

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


def split_paragraph(paragraph):
    """ Takes a paragraph and splits it into as many paragraph elements
    as possible.

    :param paragraph: A list of paragraph elements
    :return: An expanded list of paragraph elements
    """

    new_paragraph = []

    for paragraph_element in paragraph:
        if paragraph_element['kind'] is "code":
            new_paragraph.append(paragraph_element)
            continue

        if paragraph_element['kind'] is "list":

            items = []
            for item_paragraphs in paragraph_element['items']:
                new_item_paragraphs = []
                for item_paragraph in item_paragraphs:
                    new_item_paragraphs.append(
                        split_paragraph(paragraph=item_paragraph))
                items.append(new_item_paragraphs)

            paragraph_element['items'] = items

            new_paragraph.append(paragraph_element)
            continue

        if "link" in paragraph_element:
            new_paragraph.append(paragraph_element)
            continue

        new_paragraph += split_text(paragraph_element)

    return new_paragraph


def join_paragraph(paragraph):
    """ Takes a paragraph and joins it into as few paragraph elements
    as possible.

    :param paragraph: A paragraph
    :return: An reduced paragraph
    """

    new_paragraph = []

    # We use this item to accumulate the content from adjacent
    # text elements
    text = []

    def _flush(paragraph, text):
        if text:
            paragraph.append(
                {'kind': 'text', 'content': " ".join(text)})

            # Remove all elements in the list
            del text[:]

    flush = functools.partial(_flush, paragraph=new_paragraph, text=text)

    for paragraph_element in paragraph:

        if paragraph_element['kind'] is "code":
            flush()
            new_paragraph.append(paragraph_element)
            continue

        if paragraph_element['kind'] is "list":

            # A list contains even more paragraphs
            items = []

            for item_paragraphs in paragraph_element['items']:
                new_item_paragraphs = []
                for item_paragraph in item_paragraphs:
                    new_item_paragraphs.append(
                        join_paragraph(paragraph=item_paragraph))

                items.append(new_item_paragraphs)

            paragraph_element['items'] = items

            flush()
            new_paragraph.append(paragraph_element)
            continue

        if "link" in paragraph_element:
            flush()
            new_paragraph.append(paragraph_element)
            continue

        text.append(paragraph_element['content'])

    # If anything remains in the temporary flush it out
    flush()

    return new_paragraph


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

        :return: A modified API with links expanded. The original API dict is
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

    def _map_paragraphs(self, paragraphs, scope):
        """ Find links in the 'text' elements
        :param self: The LinkMapper
        :param paragraphs: The paragraphs the find links in.
        :param scope: The scope
        """

        def _add_links(paragraph):

            for index, element in enumerate(paragraph):

                if element['kind'] is 'code':
                    continue

                if element['kind'] is 'list':

                    for item_paragraphs in element['items']:
                        for item_paragraph in item_paragraphs:
                            _add_links(item_paragraph)

                    continue

                if 'link' in element:
                    continue

                if "::" not in element['content']:
                    # We skip over stuff that does not have a scope
                    # qualifier in it. Just to avoid making random
                    # characters into links..
                    continue
                typename = element['content']
                last_char_is_punctuation = typename[-1] in ',.!?:;'
                if last_char_is_punctuation:
                    typename = typename[:-1]

                link = self._find_link(
                    typename=typename, scope=scope)

                if link:
                    if last_char_is_punctuation:
                        paragraph.insert(
                            index + 1, {'kind': 'text', 'content': element['content'][-1]})
                        element['content'] = typename

                    element['link'] = link

        new_paragraphs = []
        for paragraph in paragraphs:
            new_paragraph = split_paragraph(paragraph=paragraph)

            _add_links(paragraph=new_paragraph)

            new_paragraphs.append(join_paragraph(paragraph=new_paragraph))

        return new_paragraphs

    def _map_type(self, typelist, scope):
        """ Find links in the 'type' lists """

        # 1. Split the type into it most basic elements
        typelist = split_typelist(typelist=typelist)

        # 2. Check if we have a link for each of the items
        for item in typelist:

            if "link" in item:
                link_value = item["link"]["value"]
                # If we do have a link to a type it should be in the API
                assert link_value in self.api

                # Doxygen has a bug when a (member) function has the same name
                # as a type. In this case it can wrongfully pick the function
                # rather than the type.
                # Remove the link if this is the case:
                if self.api[link_value]['kind'] != 'function':
                    continue
                item.pop("link", None)

            link = self._find_link(typename=item['value'], scope=scope, is_type=True)

            if link is not None:
                item['link'] = link

        # 3. Reduce the typelist such that only elements with links are
        #    kept standalone
        typelist = join_typelist(typelist=typelist)

        return typelist

    def _find_link(self, typename, scope, is_type=False):
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
            # The typename was found directly in the API
            return {"url": False, "value": typename}

        if scope is None:
            # We do not have a scope so there is nothing more we can do
            return None

        scopes = split_cppscope(cppscope=scope)

        for scope in scopes:

            scoped_name = scope + '::' + typename

            if scoped_name in self.api:
                if is_type and self.api[scoped_name]['kind'] == 'function':
                    continue
                # The scope qualified name was found
                return {"url": False, "value": scoped_name}

        # Finally try the link provider - which either returns None or a link
        return self.link_provider.find_link(typename=typename)
