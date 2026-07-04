You are an engineer working on porting a legacy device configuration tool into a minimal Linux container for CI/CD testing. To test the tool without the physical device, you need to implement a mock server (emulator) that strictly adheres to the device's proprietary text-based protocol.

Your task is to write a Python 3 script at `/home/user/mock_server.py` that implements a TCP server on `127.0.0.1:8888`. It must emulate the device's state machine, parse requests, validate parameters, and strictly enforce the device's rate limits. 

Here is the specification for the protocol:
1. **Connection State:** Every new TCP connection starts in the `INIT` state.
2. **Commands (delimited by `\n`):**
   - `HELO <client_id>`
     - If in `INIT` state: Transitions to `READY` state. Responds with `ACK <client_id>\n`.
     - If already in `READY` state: Responds with `ERR 400 BAD REQUEST\n`.
   - `EXEC <command_string>`
     - If in `INIT` state: Responds with `ERR 403 FORBIDDEN\n`.
     - If in `READY` state:
       - **Validation:** `<command_string>` must contain ONLY alphanumeric characters (A-Z, a-z, 0-9). If it contains any other characters (spaces, punctuation, etc.), respond with `ERR 400 BAD REQUEST\n`.
       - **Rate Limiting:** The device only accepts up to 2 `EXEC` commands per a rolling 1.0-second window per connection. If a 3rd `EXEC` command is received within 1.0 second of the 1st `EXEC` command, respond with `ERR 429 TOO MANY REQUESTS\n` (does not execute).
       - If valid and within rate limits: Responds with `RUN <command_string>\n`.
   - `QUIT`
     - Responds with `BYE\n` and immediately closes the connection.
   - Any unknown command or unrecognized format:
     - Responds with `ERR 500 UNKNOWN\n`.

Requirements:
- Write the server entirely in Python at `/home/user/mock_server.py`.
- Ensure it can handle at least one connection at a time.
- After writing the server, start it in the background.
- Finally, test your server by running the provided integration test suite: `python3 /home/user/test_client.py`
- The `test_client.py` (already present on the system) will connect to your server, run through multiple scenarios, and create a file at `/home/user/test_report.log`.
- To succeed, the last line of `/home/user/test_report.log` must be exactly: `STATUS: ALL TESTS PASSED`

You may use standard library Python modules only (e.g., `socket`, `time`, `re`).