You are an integration developer responsible for testing a newly written Rust-based Web API. The API is designed to validate session tokens, but the developer left the project in an incomplete state. It currently has a compile-time error, and once fixed, it needs to be rigorously tested for edge-case crashes.

Your objective has three phases:

**Phase 1: Fix the Rust API**
The source code for the API is located at `/home/user/session-api/`.
1. The project fails to compile due to a Rust borrow checker / ownership error in `/home/user/session-api/src/main.rs`.
2. Identify and fix the memory ownership issue so the project compiles successfully. Do not change the API's port (8080) or its core routing logic, just fix the compilation error.
3. Start the API server in the background using `cargo run`.

**Phase 2: Build a Bash Property-Based Tester**
Write a custom property-based testing script in Bash at `/home/user/pbt.sh`. 
Your Bash script must:
1. Implement a custom data structure logic to build JSON payloads dynamically. The payload must strictly match this format:
   `{"request_type": "validate", "payload": {"token": "<GENERATED_TOKEN>", "metadata": {"len": <LENGTH_OF_TOKEN>}}}`
2. Generate random alphanumeric tokens of varying lengths (between 5 and 15 characters).
3. Send these payloads to the API via `POST http://127.0.0.1:8080/validate` with the `Content-Type: application/json` header.
4. The API is supposed to return `200 OK` for valid tokens and `400 Bad Request` for tokens containing special characters (though your generator should only make alphanumeric ones). 
5. However, there is a hidden panic (500 Internal Server Error or dropped connection) triggered by a specific, rare property in the token string. Your fuzzer should rapidly generate and test tokens until the API crashes or returns an empty/500 response. (Hint: The bug is triggered when a token contains exactly three consecutive uppercase letters followed immediately by a digit, e.g., `abcXYZ9def`).

**Phase 3: Log the Crash**
Once your Bash script discovers a token that crashes the API or causes a 500/empty response:
1. Stop the fuzzer.
2. Write the exact JSON payload that caused the failure to a file located at `/home/user/bug_report.log`.
3. The file should contain *only* the raw JSON string on a single line.

**Constraints:**
- You must use Bash for the fuzzer (`/home/user/pbt.sh`).
- You may use standard Linux utilities (`curl`, `tr`, `head`, `urandom`, `jq`, `awk`, etc.).
- Do not modify the API's panic logic; your job is to discover it using the Bash script.