import wurfapi.collapse_inline_namespaces


def test_nested_ab_namespace(datarecorder):

    api = {
        "A": {"scope": None, "kind": "namespace", "inline": False, "members": ["A::B"]},
        "A::B": {
            "scope": "A",
            "kind": "namespace",
            "inline": True,
            "members": ["A::B::foo"],
        },
        "A::B::foo": {"scope": "A::B", "kind": "class"},
    }

    api = wurfapi.collapse_inline_namespaces.collapse_inline_namespaces(
        api, selectors=["A::B"]
    )

    datarecorder.recording_path = "test/data/recordings/test_nested_ab_namespace.json"
    datarecorder.record(data=api)


def test_nested_a_namespace(datarecorder):

    api = {
        "A": {"scope": None, "kind": "namespace", "inline": True, "members": ["A::B"]},
        "A::B": {
            "scope": "A",
            "kind": "namespace",
            "inline": False,
            "members": ["A::B::foo"],
        },
        "A::B::foo": {"scope": "A::B", "kind": "class"},
    }

    api = wurfapi.collapse_inline_namespaces.collapse_inline_namespaces(
        api, selectors=["A"]
    )

    datarecorder.recording_path = "test/data/recordings/test_nested_a_namespace.json"
    datarecorder.record(data=api)
