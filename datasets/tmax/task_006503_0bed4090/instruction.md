You are an integration developer testing a new Mathematical Operations API that streams calculations over WebSockets.

Your task involves setting up the environment, capturing the streaming data, performing the math locally using Bash tools, and generating a patch file of the discrepancies between the API's actual mathematical results and a flawed "expected" baseline document.

Follow these steps:

1. **Start the API Server:**
   There is a Python script located at `/home/user/api_server.py`. 
   First, install its required dependency by running `pip install websockets` (use `--break-system-packages` if required, or a venv). 
   Run the server in the background: `python3 /home/user/api_server.py &`. It will host a WebSocket server at `ws://localhost:8765`. 
   The server accepts a connection, streams exactly 20 JSON messages, and then closes the connection.

2. **Capture and Parse the Stream:**
   Connect to `ws://localhost:8765` to capture the stream. You will need a WebSocket client. You may download and use `websocat` (e.g., via `wget https://github.com/vi/websocat/releases/download/v1.11.0/websocat.x86_64-unknown-linux-musl -O websocat && chmod +x websocat`).
   The stream emits JSON objects in this format:
   `{"id": "01", "expr": "15 * 4"}`

3. **Calculate and Sort:**
   Using a Bash script (leveraging tools like `jq` and `bc`), parse the captured JSON, calculate the mathematical result of the `expr` field for each message, and format your output as a space-separated list: `[id] [result]` (e.g., `01 60`).
   Sort the final list numerically by the `id` field and save it to `/home/user/actual_results.txt`.

4. **Generate a Patch:**
   There is an existing file at `/home/user/expected_results.txt` containing the supposed baseline calculations. However, some of these expected results are incorrect.
   Compare your computed `/home/user/actual_results.txt` against `/home/user/expected_results.txt`.
   Use the `diff` command in unified format to generate a patch file that would update `expected_results.txt` to match your `actual_results.txt`.
   Save this patch to `/home/user/api_math.patch`.
   *(Hint: `diff -u /home/user/expected_results.txt /home/user/actual_results.txt > /home/user/api_math.patch`)*

Ensure your final patch file is correctly saved at `/home/user/api_math.patch`.