def pytest_configure(config):
    config.addinivalue_line(
        "markers", "download_test: This test uses the network.")

    config.addinivalue_line(
        "markers", "ensure_doxygen: This test uses the network.")