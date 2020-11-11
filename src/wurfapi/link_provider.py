import os
import re
import copy

cppreference_mappings = [
    {
        "pattern": "(std::)?u?int\d*_t",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/types/integer"}
    },
    {
        "pattern": "(std::)?size_t",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/types/size_t"}
    },
    {
        "pattern": "std::(vector|map|array|deque|forward_list|list|set)",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/container/{0}"}
    },
    {
        "pattern": "std::string",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/string/basic_string"}
    },
    {
        "pattern": "std::function",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/utility/functional/function"}
    },
    {
        "pattern": "(float|double|int|bool)",
        "link": {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/language/types"}
    },
]


class LinkProvider(object):

    def __init__(self, user_mappings):
        self.user_mappings = user_mappings

    def find_link(self, typename):
        """ Given a token e.g. std::function see if we can find a link

       First we check if the type name is found in the user mapping. After
       this we try our default mappings.

       :param typename: A C++ type name as a string
       :return: A link dictionary or None
       """

        mappings_list = [self.user_mappings, cppreference_mappings]

        for mappings in mappings_list:
            link = self._check_mapping(mappings=mappings, typename=typename)

            if link:
                return link

        return None

    def _check_mapping(self, mappings, typename):

        for mapping in mappings:
            match = re.match(mapping["pattern"], typename)

            if match:

                # We take the link dictionary and try to replace any format
                # strings with the match (if any)
                link = copy.deepcopy(mapping["link"])

                # The match.groups() returns a tuple with all the matching
                # groups. We unpack that and pass it to format which allows
                # us to write links like "http://somereference.com/{0}" where
                # {0} gets replaced with the content for the first match group
                # and so forward. If there are no match groups nothing gets
                # replaced.
                link["value"] = link["value"].format(*match.groups())

                return link

        return None
