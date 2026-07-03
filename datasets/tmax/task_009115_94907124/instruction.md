You are a script developer working on security utilities for a real-time chat application. The application uses WebSockets for communication and a SQLite database for storage. Recently, a custom C shared library was introduced for cryptographic hashing, but the integration is incomplete.

You need to fix the build process, perform a database schema migration, and write a property-based testing utility to fuzz the WebSocket server. 

Your tasks are:

1. **Fix the Build System (Shared Library Linking)**
In `/home/user/app/ext/`, there is a Python C-extension (`sec_ext.c`) and a `setup.py` script. The extension relies on a custom shared library located at `/home/user/app/lib/libcustomsec.so`. Currently, building and importing this module fails because the shared library cannot be found at runtime. 
Modify `/home/user/app/ext/setup.py` so that the extension is correctly linked to the shared library. You **must not** rely on or modify the `LD_LIBRARY_PATH` environment variable. Instead, configure the build script to embed the exact runtime search path (rpath) pointing to `/home/user/app/lib`. Once fixed, install the extension into the current Python environment so that `import sec_ext` works globally.

2. **Database Schema Migration**
The application uses a SQLite database at `/home/user/app/db/chat.db`. The `messages` table currently has the schema: `(id INTEGER PRIMARY KEY, content TEXT)`.
Write a migration script at `/home/user/app/migrate.py` that:
- Connects to the database.
- Adds a new column `msg_hash` (TEXT) to the `messages` table.
- Backfills the new column for all existing rows. For each row, calculate the hash of the `content` using the newly installed extension (`sec_ext.compute_hash(content)`) and store it in `msg_hash`.

3. **Property-Based Testing for WebSocket Communication**
We need a test script to ensure the WebSocket server handles unexpected inputs robustly. 
Write a test script at `/home/user/app/test_ws.py` using `pytest`, `pytest-asyncio`, and the `hypothesis` library. 
The test should:
- Include an async test function `test_websocket_payloads`.
- Use Hypothesis to generate JSON payloads consisting of an integer `id` and a string `content` (e.g., `{"id": 123, "content": "test"}`).
- Connect to a local WebSocket server at `ws://localhost:8080`.
- Send the generated JSON payload.
- Read the response. 
- Ensure no uncaught exceptions crash the client (the server will either return a valid JSON response or close the connection with an error code, both of which are acceptable).
Write the file so it can be successfully executed via `pytest /home/user/app/test_ws.py`.

Make sure all scripts are properly formatted and executable. You do not need to start the WebSocket server yourself; just write the test script.