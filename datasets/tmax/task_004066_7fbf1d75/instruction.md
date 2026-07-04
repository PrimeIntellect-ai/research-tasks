You are acting as a QA engineer setting up a test environment for a distributed calculator application. The frontend team needs a mock backend to test their WebSocket integration. The real backend evaluates mathematical expressions, but for this test environment, you need to build a lightweight emulator.

Your task is to:
1. Write a Python WebSocket server script at `/home/user/ws_mock.py` that listens on `ws://localhost:9090`.
2. The server must accept incoming text messages representing mathematical expressions in Prefix (Polish) notation. 
3. The expressions will consist of integers and the operators `+`, `-`, `*`, and `/` separated by single spaces. 
   Example input: `* + 2 3 4` (which evaluates to `(2 + 3) * 4`).
4. The server must parse and evaluate the expression, and send back the result as a string formatted to one decimal place (e.g., `"20.0"`).
5. Start the server in the background.
6. Write a small Python client script at `/home/user/client.py` that connects to the server, sends the exact expression `- * + 5 10 2 8`, receives the evaluated response, and saves the exact response text to `/home/user/ws_output.txt`.
7. Run the client script so that `/home/user/ws_output.txt` is populated.

You may need to install the `websockets` library using `pip` before you begin. Ensure the server gracefully handles the specific test expression.