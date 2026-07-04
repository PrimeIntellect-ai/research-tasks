You are an integration developer responsible for migrating a legacy API mocking framework and testing it with a custom testing Domain Specific Language (DSL). 

You have been provided an SQLite database at `/home/user/api.db`. This database contains a table named `mocks_v1` with the following schema:
`id INTEGER PRIMARY KEY, endpoint TEXT, payload_encoded TEXT`

The `payload_encoded` column contains a hex string. When decoded from hex to bytes, it represents a string encoded in **UTF-16LE**. 
The decoded string always follows the exact format: `status=<integer>,body=<string>`.

Your objectives are as follows:

1. **Schema Migration & Data Decoding:**
Write a Python script at `/home/user/migrate.py` that connects to `/home/user/api.db`. 
It should create a new table named `mocks_v2` with the schema:
`id INTEGER PRIMARY KEY, endpoint TEXT, status_code INTEGER, response_body TEXT`
The script must read all rows from `mocks_v1`, decode the `payload_encoded` strings, parse out the status code (as an integer) and the response body (as a string), and insert the structured data into `mocks_v2`. Ensure the `id` and `endpoint` match the original rows.

2. **DSL Interpreter / Emulator:**
You have a test file written in a custom DSL at `/home/user/queries.dsl`.
The DSL consists of pairs of lines. The first line of a pair specifies the endpoint to execute, and the second specifies the expected HTTP status code.
Example syntax:
```text
EXEC /api/v1/auth
ASSERT_STATUS 200
```
Write a Python script at `/home/user/emulator.py` that parses and interprets this DSL file. For each pair of instructions, the interpreter must:
- Query the newly migrated `mocks_v2` table in `/home/user/api.db` for the given endpoint.
- If the endpoint is not found in the database, output exactly: `[<endpoint>] ERROR: not found`
- If the endpoint is found, compare the `status_code` in the database to the `ASSERT_STATUS` value.
- If they match, output exactly: `[<endpoint>] PASS: <response_body>`
- If they do not match, output exactly: `[<endpoint>] FAIL: expected <assert_status_value>, got <database_status_value>`

The emulator must write these outputs, line by line in the order they appear in the DSL, to a log file at `/home/user/test_results.log`.

Run both of your scripts (`migrate.py` and `emulator.py`) so that the `mocks_v2` table is fully populated and `/home/user/test_results.log` is generated with the final output.