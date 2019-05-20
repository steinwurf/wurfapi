

def next_inline_namespace(api):

    for key, value in api.items():
        if value["kind"] != "namespace":
            continue

        if value["inline"] == False:
            continue

        return key


def update_scope(api, from_scope, to_scope):

    def _update(value):
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = _update(v)

            return value

        if isinstance(value, list):
            return [_update(v) for v in value]

        if value.startswith(from_scope):
            return value.replace(from_scope, to_scope, 1)
        else:
            return value

    api = copy.deepcopy(api)

    return _update(api)


def remove_inline_namespace(api):

        


def collapse_nested_namespaces(api):
    """ Collapses nested namespaces.

    This function transforms the API JSON, this is done by:
    1. Remove the name of the nested namespace in the scope of the members.
    2. Removing any namespaces that are marked inline.
    """

    inline_namespaces = []

    for key, value in api.items():
        if value["kind"] != "namespace":
            continue

        if value["inline"] == False:
            continue

        inline_namespaces.append(key)

    from_scope = key
    to_scope = api[key]['scope']

    # A::B::A::B::A
    # A::B::A -> A::B

    # A::B::B::A
    # A::B::B -> A::B


def test_check_schema():

    wurfapi.check_api_schema.check_api_schema(api=test_api)
