You are migrating an old API gateway component from Python 2 to Python 3. The codebase relies on a custom C-extension and Python routing library that passes tests locally on the old stack but fails in the new Python 3 CI environment. 

Your objective is to fix the vendored package for Python 3, and then write a firewall script that parses incoming requests to detect malicious payloads.

**Step 1: Fix and Install the Vendored Package**
A custom routing package `legacy_router` is vendored at `/app/legacy_router`. It currently fails to build and import on Python 3 due to two issues:
1. The `Makefile` relies on Python 2 build tools. Update it to use Python 3 configuration tools.
2. The package suffers from a Python 2 relative import issue (masking a standard library module) which causes an `ImportError` on Python 3.

Fix the package source and install it globally or in the user environment so that `import legacy_router` works in Python 3.

**Step 2: Implement the Firewall Script**
Write a script at `/home/user/evaluate_requests.py` that takes a single command-line argument: the path to a text file containing one URL per line.

For each URL:
1. Use `legacy_router.parse_url(url)` to extract the query parameters. This function returns a dictionary.
2. Extract the `bytecode` query parameter. It contains a Base64-encoded string representing a custom query mini-language.
3. Decode the Base64 string. The resulting plaintext consists of instructions separated by the pipe character `|`. Each instruction is formatted as `COMMAND ARGUMENT` (separated by a single space).
4. Emulate the execution flow by parsing the commands to determine if the payload is malicious.

**Malicious Payload Rules (Reject if any apply):**
- The command is `EXEC`.
- The command is `READ` or `WRITE` and the argument contains a directory traversal sequence (`..`).
- The command is `READ` or `WRITE` and the argument is an absolute path that does NOT start exactly with `/data/public/`. (Relative paths without `..` are considered safe).

**Output Format:**
For each URL in the input file, your script must print exactly one line to standard output:
- `ACCEPT` if the payload violates none of the rules.
- `REJECT` if the payload violates any of the rules.
- If the URL fails to parse, or the `bytecode` parameter is missing/malformed, default to `REJECT`.

You are provided with a training set of URLs to test your script:
- Clean: `/app/training_corpus/clean/urls.txt`
- Evil: `/app/training_corpus/evil/urls.txt`

Your solution will be evaluated against a hidden, similarly structured adversarial corpus.