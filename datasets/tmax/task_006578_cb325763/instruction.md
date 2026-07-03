You are a platform engineer maintaining a CI/CD pipeline for an API gateway. The gateway needs to route requests to different backend services based on the semantic version of the client making the REST API request.

To perform property-based testing on the API gateway's routing logic, we need a fixture generator. 

Write a pure Bash script located at `/home/user/fuzz_routing.sh` that generates a test suite of random REST API payloads. 

The script must do the following when executed:
1. Generate exactly 100 random, valid semantic versions (`Major.Minor.Patch`). 
   - `Major` must be a random integer between 0 and 3 (inclusive).
   - `Minor` must be a random integer between 0 and 15 (inclusive).
   - `Patch` must be a random integer between 0 and 15 (inclusive).
2. For each generated version, perform a strict Semantic Version comparison against the baseline version `1.10.5`.
3. If the generated version is greater than or equal to `1.10.5` (e.g., `2.0.0`, `1.11.0`, `1.10.12`), the expected routing action is `route_v2`.
4. If the generated version is strictly less than `1.10.5` (e.g., `1.9.15`, `0.15.0`, `1.10.4`), the expected routing action is `route_v1`.
5. Append a constructed JSON object for each generated version to the file `/home/user/routing_tests.jsonl`. Each object must be on its own line (JSONL format) and look exactly like this:
   `{"client_version": "X.Y.Z", "expected_routing": "ACTION"}`
   (Replace `X.Y.Z` with the generated version and `ACTION` with the evaluated routing action).

Requirements:
- Ensure the script is executable (`chmod +x`).
- The file `/home/user/routing_tests.jsonl` should be created or overwritten each time the script runs.
- Do not use Python, Ruby, or Node.js; use Bash and standard Linux tools (like `awk`, `sed`, or pure bash logic) to perform the semantic version comparison and JSON construction.
- Make sure the logic accurately handles multi-digit semver comparisons (e.g., `1.2.0` is less than `1.10.0`).