
import schema
import copy
import six

# def next_inline_namespace(api):

#     for key, value in api.items():
#         if value["kind"] != "namespace":
#             continue

#         if value["inline"] == False:
#             continue

#         return key


# def remove_inline_namespace(api):
#     pass


# def collapse_nested_namespaces(api):
#     """ Collapses nested namespaces.

#     This function transforms the API JSON, this is done by:
#     1. Remove the name of the nested namespace in the scope of the members.
#     2. Removing any namespaces that are marked inline.
#     """

#     inline_namespaces = []

#     for key, value in api.items():
#         if value["kind"] != "namespace":
#             continue

#         if value["inline"] == False:
#             continue

#         inline_namespaces.append(key)

#     from_scope = key
#     to_scope = api[key]['scope']


# class Node(object):

#     def __init(self, scope):
#         self.scope = scope
#         self.children = []

#     def add_sc

class Trie(object):

    def __init__(self):
        self.scopes = {}

    def add_scope(self, scope):

        elements = scope.split("::")

        current_scope = self.scopes

        for element in elements:

            if element in current_scope:
                current_scope = current_scope[element]
            else:
                current_scope[element] = {}
                current_scope = current_scope[element]

    def to_string(self):

        def go_deep(scope):

            _scope = []

            for key in scope:

                _scope.append([key])

                if len(scope[key]):

                    _scope += go_deep(scope[key])


# We want to collapse inline namespaces in "most" to "least" nested. This
# ensures we have a stable scope prefix to look for.
#
# Example:
#
#     namespace A
#     {
#         inline namespace B
#         {
#             inline namespace C
#             {
#             }
#         }
#     }
#
# In this case we have 3 possible scopes "A", "A::B", and "A::B::C".
#
# If we start by collapsing "A::B" to "A" then we will run into trouble when
# we want to collapse "A::B::C" to "A::B". However, if we start by collapsing
# "A::B::C" to "A::B" and then collapse "A::B" to "A". We should be good.
#
# So how do find the most nested prefix. If we think of the scopes as a tree, we
# want to start at the leafs and then work backwards.
#
# If we just use the length of the scope and start with the longest we are
# guarenteed to start at a leaf since if any inline namespaces are less nested
# then it is also guarenteed to have a shorter scope name since the namespaces
# share a common prefix.
#


def update_scope(api, from_scope, to_scope):

    def _collapse(value):
        if value.startswith(from_scope):
            return value.replace(from_scope, to_scope, 1)
        else:
            return value

    def _update(value):
        if isinstance(value, dict):

            result = {}

            for old_key, old_value in value.items():

                new_key = _collapse(value=old_key)
                new_value = _update(value=old_value)

                assert new_key not in result

                result[new_key] = new_value

            return result

        if isinstance(value, list):
            return [_update(v) for v in value]

        if isinstance(value, six.string_types):
            return _collapse(value=value)

        return value

    return _update(api)


def collapse_inline_namespaces(api, selectors):
    """ Collapses inline namespaces.

    This function transforms the API JSON, this is done by:
    1. Remove the name of the inline namespace in the scope of the members.
    2. Removing any namespaces that are marked inline.
    """

    # Sort the selectors to get the most nested namespace first
    selectors.sort(key=len, reverse=True)

    for selector in selectors:

        namespace = api[selector]

        # Make sure we are selecting an inline namespace
        schema.Schema({'kind': 'namespace', 'inline': True},
                      ignore_extra_keys=True).validate(namespace)

        from_scope = selector
        to_scope = namespace['scope']

        # Remove the inline namespace from the API
        del api[selector]

        # Remove references to it
        api[to_scope]['members'].remove(selector)

        # Collapse all scopes in the API
        api = update_scope(api=api, from_scope=from_scope, to_scope=to_scope)

    return api


def test_trie():

    api = {'A': {'scope': None, 'kind': 'namespace',
                 'inline': False, 'members': ['A::B']},
           'A::B': {'scope': 'A', 'kind': 'namespace',
                             'inline': True, 'members': ['A::B::foo']},
           'A::B::foo': {'scope': 'A::B', 'kind': 'class'}}

    print(api)

    api = collapse_inline_namespaces(api, selectors=['A::B'])

    print(api)

    assert(0)
