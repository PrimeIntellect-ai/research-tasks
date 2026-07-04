You are a platform engineer maintaining a CI/CD pipeline. One of your data processing steps requires migrating a configuration schema, verifying its integrity using a custom legacy C library, and exposing the result via a minimal REST API for downstream services.

You have been provided with the following files:
1. `/home/user/schema_v1.json`: A legacy configuration file.
2. `/home/user/src/checksum.c`: A C source file containing a legacy error-checking algorithm.

Your task is to:
1. Compile `/home/user/src/checksum.c` into a shared library named `/home/user/lib/libchecksum.so`.
2. Write a script (in Python, Node.js, or Ruby) that loads this shared library via FFI (Foreign Function Interface) / ctypes.
3. Read the `/home/user/schema_v1.json` file and perform the following schema migration in memory:
   - Rename the top-level key `users` to `account_holders`.
   - Add a new top-level key `version` with the integer value `2`.
   - Completely remove the top-level key `legacy_flag`.
4. Serialize the migrated schema back to a JSON string. The JSON string MUST have no whitespace between elements and its keys MUST be sorted alphabetically.
5. Pass this exact minimized, sorted JSON string to the `compute_checksum(const char* data, int len)` function from your compiled shared library to calculate its integrity checksum.
6. Start a background REST API server listening on `127.0.0.1:8080`.
7. The API must have a single endpoint: `GET /schema/v2`. When called, it must return a JSON response with HTTP status 200 and the following structure:
   ```json
   {
     "checksum": <calculated_integer_checksum>,
     "data": <the_migrated_schema_object>
   }
   ```
   *(Note: `data` here should be the actual JSON object, not a stringified version).*
8. Once your server is up and listening on port 8080, create an empty file at `/home/user/server_ready.txt` to signal to the pipeline that the service is ready.

Leave the server running in the background. Do not block the terminal.