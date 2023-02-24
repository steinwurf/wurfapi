import os
import json


def test_run(testdirectory):

    testdirectory.run("python -m wurfapi")
    testdirectory.run("wurfapi")


def test_build_docs(testdirectory, datarecorder):

    cpp_coffee = testdirectory.copy_dir(directory="test/data/cpp_coffee")

    # Make it a git repo - we will try to fetch the project root from git
    cpp_coffee.run(["git", "init"])
    cpp_coffee.run(["git", "add", "."])
    cpp_coffee.run(
        [
            "git",
            "-c",
            "user.name=John",
            "-c",
            "user.email=doe@email.org",
            "commit",
            "-m",
            "oki",
        ]
    )

    docs = cpp_coffee.join("docs")
    docs.run("sphinx-build --no-color -w log.txt -vvv -b html . _build")
    log_file = os.path.join(docs.path(), "log.txt")

    # The log file should have zero size - i.e. now warnings or errors..
    # As you can see we are not quite there :)
    with open(log_file, "r") as log:
        log_data = log.read()

    datarecorder.record_data(
        data=log_data, recording_file="test/data/log_recordings/log.txt"
    )

    # Find and track changes to the wurfapi json file. This is the final API
    # output produced after parsing the sources and running our various steps
    # to transform the output.
    wurfapi_json_file = os.path.join(
        docs.path(), "_build", ".doctrees", "wurfapi_api.json"
    )

    with open(wurfapi_json_file, "r") as wurfapi_json:
        wurfapi_data = json.load(wurfapi_json)

    datarecorder.record_data(
        data=wurfapi_data, recording_file="test/data/build_coffee_wurfapi.json"
    )
