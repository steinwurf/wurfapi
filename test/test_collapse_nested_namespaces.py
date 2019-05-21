

# def next_inline_namespace(api):

#     for key, value in api.items():
#         if value["kind"] != "namespace":
#             continue

#         if value["inline"] == False:
#             continue

#         return key


# def update_scope(api, from_scope, to_scope):

#     def _update(value):
#         if isinstance(value, dict):
#             for k, v in value.items():
#                 value[k] = _update(v)

#             return value

#         if isinstance(value, list):
#             return [_update(v) for v in value]

#         if value.startswith(from_scope):
#             return value.replace(from_scope, to_scope, 1)
#         else:
#             return value

#     api = copy.deepcopy(api)

#     return _update(api)


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


def test_trie():

    trie = Trie()

    trie.add_scope("A::B::C")
    trie.add_scope("A::D")

    print(trie.scopes)

    assert(0)
