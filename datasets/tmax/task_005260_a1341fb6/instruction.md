You are a script developer building an automated testing utility for a web security scanner. Your objective is to create a mock exploit payload and a test harness that simulates a security breach reporting mechanism.

Perform the following steps:

1. **Create and Compile a Minimal Payload (C)**
   Write a C program at `/home/user/payload.c` that prints a JSON string to standard output. 
   - If compiled normally, it should print: `{"status": "exploited", "env": "production"}`
   - If compiled with the preprocessor macro `MOCK_MODE` defined, it should print: `{"status": "exploited", "env": "staging"}`
   - Compile this C program into a statically linked executable at `/home/user/payload.bin`. You MUST compile it with the `MOCK_MODE` macro defined (e.g., using `-DMOCK_MODE`).

2. **Develop the Test Harness (Python)**
   Write a Python script at `/home/user/test_harness.py` that performs the following:
   - **Parse structured data:** Read the WAF log file located at `/home/user/waf_logs.json`. This file contains a list of JSON objects representing web requests. Extract a unique list of all `user_agent` strings from entries where the `"action"` field is exactly `"blocked"`. Sort this list alphabetically.
   - **Test Fixture Setup:** Spin up a background HTTP server in the script (e.g., using `http.server` or `wsgiref`) listening on `127.0.0.1` port `8000`. 
   - **Payload Execution:** Run the compiled `/home/user/payload.bin` executable as a subprocess and capture its standard output. Parse this output as JSON.
   - **Integration:** From the main thread of your Python script, send an HTTP POST request to `http://127.0.0.1:8000/report` with a JSON payload in the following format:
     ```json
     {
       "payload_result": {<the JSON object returned by payload.bin>},
       "blocked_agents": ["<agent1>", "<agent2>", "..."]
     }
     ```
   - **Mock Server Behavior:** The mock server must accept the POST request to `/report`, read the incoming JSON body, write it exactly as received (formatted with 4-space indentation) to `/home/user/final_report.json`, and then cleanly shut down the server so the Python script can exit successfully.

3. **Execution**
   Run your Python script so that `/home/user/final_report.json` is generated.

Your final success will be verified by checking the existence, compilation parameters, and exact JSON structure of `/home/user/final_report.json`.