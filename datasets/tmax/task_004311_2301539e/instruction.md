You are a platform engineer responsible for maintaining our CI/CD pipeline infrastructure. We are integrating a new real-time build monitoring service that streams dependency update logs during the build phase. However, the stream is highly fragmented and we need a reliable way to parse it, evaluate semantic version changes, and generate an automated test report.

I have placed a mock WebSocket server script at `/home/user/mock_server.py`. This server simulates the build event stream. 

Your task is to write a complete Python solution that performs the following steps:

1. **Start the Mock Server**: Run `/home/user/mock_server.py` in the background. It will start a WebSocket server on `ws://localhost:8765`.
2. **Create the CI Monitor**: Write a Python script at `/home/user/ci_monitor.py` that connects to this WebSocket server.
3. **Stream Parsing (State Machine)**: The server sends text logs containing JSON objects that represent dependency updates (e.g., `{"pkg": "libA", "old": "1.2.3", "new": "1.3.0"}`). However, the WebSocket messages are artificially fragmented into random chunks of characters (e.g., chunk 1 might be `{"pkg": "li`, chunk 2 might be `bA", "old": "1.`). You must implement a parser/state machine in your client to accumulate these chunks and extract complete, valid JSON objects. The stream ends when the server sends the exact string `"EOF"`.
4. **Semantic Version Policy Evaluation**: For each successfully parsed JSON object, compare the `old` and `new` semantic versions. 
   Apply the following strict CI policy:
   - **REJECT** the update if the `new` version is a downgrade (older than the `old` version, taking pre-release tags into account if possible, though standard major.minor.patch comparison is the baseline).
   - **REJECT** the update if the `new` major version is greater than the `old` major version (we do not allow unexpected breaking changes in this pipeline).
   - **ACCEPT** all other valid updates (minor or patch upgrades).
   You may install and use external libraries like `websockets` and `packaging` to assist with this.
5. **Generate Output**: Once the `"EOF"` message is received and all objects are processed, write the final evaluation to `/home/user/ci_report.json`. The file must contain a single JSON dictionary mapping the package name (`pkg`) to either the string `"ACCEPTED"` or `"REJECTED"`.

Constraints:
- Do not modify `/home/user/mock_server.py`.
- Ensure your `ci_monitor.py` script exits gracefully after writing the report file.
- The output file `/home/user/ci_report.json` must be perfectly formatted JSON.

Execute your solution and ensure `/home/user/ci_report.json` is generated successfully.