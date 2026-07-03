You are a mobile build engineer maintaining our CI/CD pipelines. We have a multi-stage pipeline verification task that involves extracting metadata from a UI test recording, migrating a legacy hashing script, and writing a rigorous dependency update verifier.

Your objectives:

1. **Extract Metadata from Video:**
   During our automated Android UI tests, a QR code containing critical build metadata flashes on the screen. The screen recording is located at `/app/ui_test_recording.mp4`. Extract the frames (e.g., using `ffmpeg`) and decode the QR code (you may install and use `pyzbar` and `Pillow`). 
   The QR code contains a string in the format: `ROOT:<module_name>`. Note this root module name.

2. **Translate Legacy Hashing Logic:**
   Our dependency graph integrity relies on a custom checksum algorithm currently implemented in Node.js at `/app/legacy_hash.js`. Translate this entire file into Python. Your translated implementation should be saved to `/home/user/pipeline/hash.py` and contain a function `calculate_hash(data: str) -> str`.

3. **Build the Dependency Verifier:**
   Create a script at `/home/user/pipeline/verifier.py`. This script will be invoked from the command line with a single argument: the path to a proposed dependency graph JSON file (e.g., `python3 /home/user/pipeline/verifier.py update.json`).
   
   The JSON file contains a dictionary mapping module names to an object with `"deps"` (a list of string dependencies) and an `"expected_hash"` (string).
   
   Your `verifier.py` must:
   - Parse the provided JSON file.
   - Start at the root module (extracted from the video).
   - Traverse the dependency graph to find all transitive dependencies of the root module.
   - **Reject** (exit code 1) the update if there is any circular dependency (cycle) in the subgraph reachable from the root module.
   - Collect the names of all modules in the reachable subgraph (including the root itself), sort them alphabetically, and join them with commas (e.g., `module_a,module_b,module_z`).
   - Use your translated `calculate_hash` function to compute the checksum of this joined string.
   - **Reject** (exit code 1) the update if the computed checksum does not match the `"expected_hash"` defined in the root module's JSON entry.
   - **Accept** (exit code 0) the update if the graph is a valid DAG and the checksum is correct.

Ensure your `verifier.py` is robust, as it will be tested against a battery of valid and malicious dependency updates. All your work should be placed in `/home/user/pipeline/`.