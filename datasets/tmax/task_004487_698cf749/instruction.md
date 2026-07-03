You are a mobile build engineer maintaining our CI pipelines. We have a pipeline service that validates incoming code diffs (patches) to ensure developers aren't accidentally modifying sensitive build signing configurations before the changes are built.

We need you to build a local REST API that validates these patches, but there are two problems you must solve:

1. **Fix the Vendored Dependency:** 
We vendor a Python package called `patch-processor` located at `/app/vendored/patch-processor/`. Unfortunately, the latest version has a circular import bug that causes an `ImportError` when you try to `import patch_processor`. You need to diagnose and fix this circular dependency within the vendored source code so it can be imported properly. You can install it locally via `pip install -e /app/vendored/patch-processor/` once fixed.

2. **Build the Validation API:**
Create a Python REST API (using FastAPI, Flask, or standard library) in `/home/user/api.py` that listens on `127.0.0.1:8000`. 
It must expose a single endpoint: `POST /validate-patch`
- The endpoint will receive raw Unified Diff text in the request body (Content-Type: text/plain).
- You must use the fixed `patch_processor.parse(diff_text)` function to extract the list of modified file paths. (The `parse` function returns a list of string filepaths modified in the diff).
- **Validation Rules:** Your API must reject the patch if it modifies any file whose path:
  - Contains directory traversal sequences (e.g., `../` or `..\\`)
  - Starts with or contains the directories `ios/Secrets/`, `android/keystores/`, or `.github/workflows/`
- **Responses:**
  - Return HTTP 200 OK if the patch is safe (clean).
  - Return HTTP 403 Forbidden if the patch violates any of the rules (evil).

You must start this server in the background so it is actively listening on port 8000 when you complete the task. We will run an automated test suite against your API using a corpus of safe and malicious patch files.