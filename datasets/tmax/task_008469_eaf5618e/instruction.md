You are a script developer building local utilities for a development team. We are upgrading our user database schema and need a utility that can perform the schema migration on the fly and serve it to our new frontend for testing. 

Your task is to create a Python script that reads legacy JSON data, migrates it to a new schema, and serves it over HTTP. Then, create an end-to-end test script to verify it.

**Step 1: The Migration & Serving Script**
Create a Python script at `/home/user/schema_migrator.py`. 
The script must read the legacy data located at `/home/user/legacy_data.json` (you don't need to create this file, assume it exists and contains a JSON array of user objects).

Legacy schema format:
`{"full_name": "String", "birth_year": "String", "id": "String"}`

The script should deserialize this data, apply the following migration rules, and serialize it to a new JSON structure:
1. `first_name` (String): The first word of `full_name`.
2. `last_name` (String): Everything after the first space in `full_name`.
3. `age` (Integer): Calculated by subtracting `birth_year` from the fixed year `2024`.
4. `identifier` (Integer): The integer representation of `id`.

Example migrated object: `{"first_name": "John", "last_name": "Doe", "age": 34, "identifier": 101}`

The Python script must launch an HTTP server on port `8080` and serve the migrated JSON array with a `Content-Type: application/json` header whenever a `GET` request is made to `/api/v2/users`.

**Step 2: End-to-End Test Orchestration**
Create a Bash script at `/home/user/run_e2e.sh`.
This script must orchestrate the following:
1. Start the `/home/user/schema_migrator.py` server in the background.
2. Wait briefly to ensure the server is listening (e.g., `sleep 2`).
3. Use `curl` to fetch `http://localhost:8080/api/v2/users` and save the output exactly to `/home/user/migrated_response.json`.
4. Kill the background Python server gracefully.

Make sure your shell script is executable. Run `/home/user/run_e2e.sh` so that `/home/user/migrated_response.json` is generated for verification.