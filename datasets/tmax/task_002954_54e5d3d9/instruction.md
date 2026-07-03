You are an integration developer tasked with testing a new custom API. As part of this, your team has provided a highly optimized Python extension written in Rust, located in `/home/user/fastparser_ext`. This extension implements a custom state machine parser for the API protocol.

However, the package is currently broken:
1. Running `pip install .` inside `/home/user/fastparser_ext` fails due to missing build system dependencies and linking configurations.
2. The Rust code itself (`src/lib.rs`) has a deliberate ownership and borrow checker error within the state machine parser logic.

Your tasks are:
1. Fix the build system configuration in `/home/user/fastparser_ext/pyproject.toml` so that the Rust extension can be correctly compiled and linked (hint: it uses PyO3 and setuptools-rust).
2. Fix the ownership/borrow checker error in `/home/user/fastparser_ext/src/lib.rs`. Ensure the state machine logic correctly parses custom protocol strings (which are delimited by `|`) without losing data or causing compilation failures.
3. Successfully build and install the `fastparser` package in your Python environment.
4. Write a Python script at `/home/user/test_api.py` that imports the `fastparser` module and uses it to parse the following API response string:
   `"INIT_CONN|FETCH_RECORDS|UPDATE_STATE|TERMINATE|"`
5. The script must output the resulting parsed tokens as a JSON formatted array (list of strings) to `/home/user/parsed_output.json`.

Ensure your Python script is executed and `/home/user/parsed_output.json` is created with the exact correct list of commands extracted from the protocol string.