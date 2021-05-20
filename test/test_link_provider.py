import wurfapi.link_provider


def test_linkprovider():

    link_provider = wurfapi.link_provider.LinkProvider(user_mappings=[])

    # Test
    result = link_provider.find_link(typename="std::vector")

    assert result == {
        "url": True,
        "value": "https://en.cppreference.com/w/cpp/container/vector",
    }

    # Test
    result = link_provider.find_link(typename="std::map")

    assert result == {
        "url": True,
        "value": "https://en.cppreference.com/w/cpp/container/map",
    }

    # Test

    typenames = [
        "uint8_t",
        "uint16_t",
        "uint32_t",
        "uint64_t",
        "int8_t",
        "int16_t",
        "int32_t",
        "int64_t",
    ]

    for typename in typenames:
        result = link_provider.find_link(typename=typename)

        assert result == {
            "url": True,
            "value": "https://en.cppreference.com/w/cpp/types/integer",
        }
