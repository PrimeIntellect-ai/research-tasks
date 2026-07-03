You are an infrastructure developer tasked with building a custom package resolution API. We have a vendored copy of the `semantic_version` Python library (version 2.10.0) located at `/app/semantic_version/`. A previous developer made some unauthorized modifications to it while attempting to optimize it, and now its dependency matching logic is broken (specifically, matching `>=` and `<=` constraints against versions is failing or returning inverted results).

Your task has three parts:

1. **Fix the Vendored Package:**
   Locate the bug introduced in the `/app/semantic_version/` source code and fix it so that version constraint satisfaction works correctly again. (Do not pip install a fresh copy; you must fix the code in `/app/semantic_version/`).

2. **Develop the Resolution API:**
   Write a Python web server in `/home/user/resolver.py` that utilizes your fixed `semantic_version` package. 
   - It must listen for HTTP requests on `127.0.0.1:8888`.
   - It must implement routing to handle a `GET /resolve` endpoint.
   - It must require an `Authorization` header with the exact value: `Bearer test-agent-token-99`. Reject unauthorized requests with a 401 status code.
   - The endpoint will receive query parameters `pkg` (the target package name) and `req` (the semantic version specifier, e.g., `>=1.2.0`).

3. **Implement Dependency Resolution Logic:**
   When a valid request is received, your server must:
   - Read the package registry from `/home/user/registry.json` (you can assume this file contains a dictionary mapping package names to dictionaries of available versions and their dependencies).
   - Find all versions of `pkg` that satisfy the `req` constraint using `semantic_version.SimpleSpec`.
   - Sort these valid versions and select the highest one.
   - Look up the dependencies for this highest version in the registry. For each dependency, find the highest version that satisfies its respective constraint. (Assume only one level of dependencies).
   - Compute a SHA256 checksum of the final resolved list. To do this, format each resolved dependency as `<pkgname>==<version>`, sort these strings alphabetically, join them with a newline `\n`, and take the SHA256 hex digest.
   - Return a JSON response with status 200 in this format:
     ```json
     {
       "resolved": {
         "target_pkg": "1.3.0",
         "dep_a": "2.1.0"
       },
       "checksum": "a1b2c3..."
     }
     ```

Keep the server running in the foreground or background so that our automated test suite can query `127.0.0.1:8888` to verify your implementation.