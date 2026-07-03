You are an integration developer tasked with building a local CI/CD verification step for a new mathematical evaluation API. We have a Rust client that interacts with this API and relies on a proprietary C library for custom checksum validation. The project is currently failing to build and run because the shared library cannot be found at link or runtime, and the client code itself is incomplete.

Your task is to set up the mock API, complete the Rust client, fix the linking issues, and wrap it all in a CI shell script.

Here are the requirements:

1. **Workspace:** Work inside `/home/user/workspace/`.
2. **The C Library (`libverify.so`):**
   - We will assume a C library exists at `/home/user/workspace/lib/libverify.so`.
   - It exposes a single function: `uint32_t calculate_checksum(const char* input);`
   - You need to ensure the Rust project can link to this library both at compile time and runtime.
3. **The Mock API:**
   - Write a mock server (e.g., using a simple Python script `mock_api.py`) that listens on `127.0.0.1:8080`.
   - When a GET request is made to `/task`, it must return a JSON response exactly like this:
     `{"id": 42, "expression": "15 * 3 + 2", "checksum": 3283}`
   - *Note: You can hardcode this exact response for the mock.*
4. **The Rust Client (`expr_client`):**
   - Create a Rust project at `/home/user/workspace/expr_client`.
   - The client should make an HTTP GET request to `http://127.0.0.1:8080/task`.
   - Parse the JSON response.
   - Evaluate the mathematical expression. It will only contain integers, addition (`+`), and multiplication (`*`), and should follow standard order of operations. (e.g., "15 * 3 + 2" = 47).
   - Format a verification string exactly as: `id:<ID>,result:<RESULT>` (e.g., `id:42,result:47`).
   - Pass this string to the C library's `calculate_checksum` via FFI.
   - If the calculated checksum matches the API's provided checksum, write `SUCCESS: id=42, valid=true` to `/home/user/workspace/ci_report.txt`. If not, write `FAILURE`.
5. **The CI Script (`ci_run.sh`):**
   - Write a bash script at `/home/user/workspace/ci_run.sh`.
   - It must: Start the mock API in the background, compile the Rust client, run the Rust client to produce `ci_report.txt`, and finally kill the background mock API process.
   - Ensure the script is executable and handles the necessary environment variables for the dynamic linker to find `libverify.so` at runtime.

*Important:* You must generate the C library yourself to test your code. Create `/home/user/workspace/lib/verify.c` that implements `calculate_checksum` by simply summing the ASCII values of all characters in the string, and compile it to a shared library `libverify.so`. 

Ensure that executing `/home/user/workspace/ci_run.sh` runs successfully and results in the correct line written to `/home/user/workspace/ci_report.txt`.