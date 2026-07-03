You are acting as a QA engineer setting up a local test environment for a new data processing service. We have a skeleton project in `/home/user/qa_env` that is supposed to handle schema migrations and payload validation, but the developer left it in a broken state. 

Your task is to fix the package configuration, implement the missing REST API endpoint, and run a test request to verify the service.

Here are the requirements:

1. **Fix the Package**: The `pyproject.toml` in `/home/user/qa_env` has a syntax error and is missing the `Flask` dependency. Fix the file so the project can be installed. You should install the project in the current environment (e.g., using `pip install -e .`).

2. **Complete the REST API**: Edit `/home/user/qa_env/app.py` to complete the Flask application. You need to implement a POST endpoint at `/migrate`.
   - The endpoint will receive a JSON payload representing a "v1" user record: `{"user_id": "<string>", "user_name": "<string>", "balance_cents": <integer>}`.
   - You must migrate this payload to the "v2" schema:
     - Rename `user_id` to `id` and cast it to an integer.
     - Rename `user_name` to `name` (remains a string).
     - Rename `balance_cents` to `balance_dollars` and convert it to a float (divided by 100).
   - After migrating the dictionary, you must calculate a CRC32 checksum of the resulting v2 JSON. To ensure deterministic checksums, serialize the v2 dictionary to a JSON string with no whitespace (separators `,` and `:`) and keys sorted alphabetically, then calculate the CRC32 of its UTF-8 bytes using Python's `zlib.crc32`.
   - The endpoint must return a JSON response containing two fields:
     - `"data"`: The migrated v2 dictionary object.
     - `"checksum"`: The calculated CRC32 integer.

3. **Test the Service**: 
   - Start the Flask server on port `8080` in the background.
   - Use `curl` to send the following JSON payload to the `/migrate` endpoint: `{"user_id": "892", "user_name": "Charlie", "balance_cents": 4250}`.
   - Save the raw HTTP response body directly to `/home/user/qa_env/test_result.json`.

Ensure your final `test_result.json` exactly matches the expected API output.