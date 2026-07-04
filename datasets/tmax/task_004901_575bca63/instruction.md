You are a script developer tasked with creating a robust data synchronization utility. 

We have a system with a few running services (provided in the environment):
1. A Redis server running on `127.0.0.1:6379`.
2. A WebSocket server running on `ws://127.0.0.1:8081/stream` that emits realtime schema and data updates.

You need to create a new HTTP service listening on `127.0.0.1:8080` that orchestrates these updates into a local SQLite database located at `/home/user/app/data.db`.

Your service must implement the following REST endpoints:

1. `POST /sync`
   When this endpoint is hit, your service should connect to the WebSocket server at `ws://127.0.0.1:8081/stream`.
   The WebSocket server will send a sequence of JSON messages and end with a `{"type": "done"}` message. Your service should close the WebSocket connection after receiving "done" and return an HTTP 200 response with `{"status": "success"}` to the caller.
   
   The WebSocket messages will be of the following types:
   - `{"type": "schema", "table": "<table_name>", "columns": {"<col1>": "<type1>", ...}}`: 
     Create a table in the SQLite database. Types will be `int` (map to INTEGER) or `string` (map to TEXT). The first column is always the primary key.
   - `{"type": "base_data", "table": "<table_name>", "data": {"id": <id>, ...}}`: 
     Store this base data object in Redis (use a key format like `<table_name>:<id>`) and insert it into the SQLite table.
   - `{"type": "patch", "table": "<table_name>", "id": <id>, "patch": <json_patch_array>}`: 
     Apply the RFC 6902 JSON Patch array to the baseline JSON object stored in Redis. Update the corresponding row in the SQLite database with the new values.
   - `{"type": "schema_migration", "table": "<table_name>", "changes": [{"op": "add_column", "name": "<col_name>", "datatype": "<type>"}, ...]}`: 
     Execute an `ALTER TABLE` to add the new columns to the SQLite database. Update your internal tracking so subsequent patches mapped to these columns are handled correctly.

2. `POST /query`
   Accepts a JSON body `{"query": "<valid sqlite query>"}`. 
   Executes the query against `/home/user/app/data.db` and returns an HTTP 200 response with JSON `{"results": [<array of objects, where keys are column names>]}`.

Constraints & Requirements:
- You may use any language of your choice.
- You must manage the translation of structured data and diffs cleanly.
- Redis should be used to keep the latest full JSON state of each row so that JSON patches can be correctly applied before syncing to SQLite.
- The application should stay running in the background so the verifier can interact with it. Start your HTTP server as a background process and exit the terminal when your code is ready.

Ensure your service is up and listening on port `8080` before finishing your workflow.