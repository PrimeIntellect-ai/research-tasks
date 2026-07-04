You have been assigned to migrate a legacy Python 2 routing engine to Python 3 and write a multi-language test suite to verify its correctness. 

In the directory `/home/user/legacy_router`, there is a legacy Python package containing a custom URL routing engine. This engine parses URLs, extracts query parameters, and uses a custom stack-based emulator to evaluate routing conditions.

Your objectives are:

1. **Migrate the package to Python 3:**
   - Modify `/home/user/legacy_router/setup.py` so that it is syntactically valid in Python 3 and successfully installs.
   - Fix all Python 2 specific code (e.g., imports, dictionary methods, string types) in the `legacy_router` module so it runs flawlessly on Python 3.
   - Install the package in editable mode (`pip install -e .`) within the system's default Python 3 environment.

2. **Test Fixture and Mock Setup:**
   - The package exposes a CLI tool called `legacy-router-cli`. When run as `legacy-router-cli <URL>`, it outputs the name of the matched route.
   - Create a Node.js test fixture script at `/home/user/test_suite.js`.
   - The Node.js script must execute the `legacy-router-cli` for the following URLs:
     1. `http://example.com/api?role=1&points=40`
     2. `http://example.com/api?role=2&points=150`
     3. `http://example.com/api?role=1&points=200`
   - Your Node.js script must capture the standard output (stripped of leading/trailing whitespace) of the CLI for each URL and save the mapping as a JSON object to `/home/user/test_results.json`. The keys must be the exact URLs tested, and the values must be the string output of the CLI (the matched route name).

Ensure all scripts are executable and that running `node /home/user/test_suite.js` cleanly generates the required JSON file.