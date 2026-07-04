You are a QA engineer responsible for setting up a local end-to-end test environment. You need to apply a schema migration, start a mock WebSocket server, and orchestrate a quick test to ensure the server broadcasts the correct state based on the new schema.

All files are located in `/home/user/qa_env/`.

Please perform the following steps:
1. Apply the schema migration file `/home/user/qa_env/v2_migration.sql` to the existing SQLite database `/home/user/qa_env/test_db.sqlite`.
2. Start the WebSocket server in the background by running `python3 /home/user/qa_env/mock_server.py`. The server will bind to `ws://127.0.0.1:9999`. Wait a couple of seconds for it to be fully ready.
3. Use the provided WebSocket test client by running `python3 /home/user/qa_env/ws_client.py "{\"cmd\": \"get_state\"}"`. This script connects to the server, sends the provided JSON payload, and prints the server's response to standard output.
4. Capture the exact standard output from the test client and save it to `/home/user/qa_env/e2e_result.json`.
5. Terminate the background server process to clean up the environment.

Do not modify the provided Python scripts. Your success will be verified by checking that the database migration was applied and that `/home/user/qa_env/e2e_result.json` contains the correct JSON string returned by the server.