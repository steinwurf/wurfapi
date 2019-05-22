
import schema
import six

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
    """ This function iterates though the API and substitutes the from_scope
    with the to_scope.

    So if we want to change "A::B::C" to "A::B" we run:

        update_scope(api=api, from_scope="A::B::C", to_scope="A::B")

    This function dosn't try to be clever and undestand the semantics of the
    API it just looks at the raw text. This may have to change in the future
    if we run into problems with this approach.

    :param api: The API dict
    :param from_scope: The from scope as a string
    :param to_scope: The to scope as a string
    :return: A new API dict with the updated scopes
    """

    def _collapse(value):
        if not isinstance(value, six.string_types):
            return value
        elif value.startswith(from_scope):
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

        return _collapse(value=value)

    return _update(api)


def collapse_inline_namespaces(api, selectors):
    """ Collapses inline namespaces.

    This function transforms the API JSON, this is done by:
    1. Remove the name of the inline namespace in the scope of the members.
    2. Removing any namespaces that are marked inline.

    :param api: The API dictionary
    :param selectors: A list of inline namespaces that should be collapsed
    :return: An API dictionary with the inline namespace collapsed.
    """

    # Sort the selectors to get the most nested namespace first
    selectors.sort(key=len, reverse=True)

    for selector in selectors:

        if selector not in api:
            raise RuntimeError("Could not find {} selector in API. "
                               "Available selectors are: {}".format(
                                   selector, api.keys()))

        # Make sapi[selector]e selecting an inline namespace
        schema.Schema({'kind': 'namespace', 'inline': True},
                      ignore_extra_keys=True).validate(api[selector])

        # The selector is fully qualified name of the inline namespace e.g.
        # A::B::C where C is the inline namespace
        #
        # To collapse the scope of a nested namespace is simply using the
        # replace A::B::C with A::B which is the scope of C
        #
        # If the inline namespace has no scope. We need to replace selector
        # with selector + ::
        #
        # E.g. we are collapsing an inline namespace A that contains a nested
        # type A::foo. Then the from scope is "A::" to ""

        if api[selector]['scope']:
            from_scope = selector
            to_scope = api[selector]['scope']
        else:
            from_scope = selector + "::"
            to_scope = ""

        # Remove references to it
        if to_scope:
            api[to_scope]['members'].remove(selector)
            api[to_scope]['members'] += api[selector]['members']

        # Remove the inline namespace from the API
        del api[selector]

        # Collapse all scopes in the API
        api = update_scope(api=api, from_scope=from_scope, to_scope=to_scope)

    return api
