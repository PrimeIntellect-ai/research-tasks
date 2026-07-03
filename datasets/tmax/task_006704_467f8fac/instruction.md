You are tasked with writing a Python utility to extract, merge, and validate dependencies for a legacy application where the original source code is lost, but the compiled bytecode and a partial `requirements.txt` remain.

**Background:**
A previous developer hardcoded the primary dependencies in a Python file that has since been compiled, leaving only `/home/user/legacy_app.pyc`. There is also a secondary `/home/user/requirements.txt` file containing newer, but potentially conflicting or invalid, dependencies.

Your task is to write a script that does the following:
1. **Bytecode Analysis:** Programmatically analyze `/home/user/legacy_app.pyc` using Python's built-in `dis` or `marshal` modules to extract the hidden dependencies. The bytecode contains a function that returns a list of tuples representing package names and versions (e.g., `('packageA', '1.0.0')`).
2. **Merge & Sort:** Read `/home/user/requirements.txt`. Merge its dependencies with the ones extracted from the `.pyc` file. 
   - If a package exists in both sources, the version from the `.pyc` file must take precedence.
3. **Validate with Rate-Limiting:** Validate each combined dependency against the local dependency validation API. 
   - The API is available at `http://127.0.0.1:8080/validate`.
   - Make a `GET` request with query parameters `pkg` and `ver` (e.g., `http://127.0.0.1:8080/validate?pkg=requests&ver=2.25.1`).
   - The server has a strict rate limit of **maximum 2 requests per second**. If you exceed this, it returns a `429 Too Many Requests` status. Your script must handle this gracefully and retry.
   - A `200 OK` status means the package/version combination is valid. A `400 Bad Request` means it is invalid.
4. **Output:** Write all valid dependencies to `/home/user/verified_deps.txt`, sorted alphabetically by package name, in the format `pkg==version`, with one dependency per line.

**Note:** Ensure your solution automatically waits and retries if it hits a `429` status code. The background validation server is already running.