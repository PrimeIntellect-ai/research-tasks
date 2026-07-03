You are a script developer building a testing utility for a hybrid Python/C project. 

In `/home/user/app`, there is a project that runs a WebSocket server. The server processes incoming structured JSON messages, extracts a string, and transforms it using a custom C extension (`processor`) for performance. 

Currently, the C extension has a severe memory safety issue. When a client sends a payload containing a string longer than 50 characters, the C extension causes a segmentation fault and crashes the entire WebSocket server due to a buffer overflow.

Your task is to:
1. Locate and fix the memory safety vulnerability in `/home/user/app/processor.c`. You should modify it to safely handle input strings of any length by dynamically allocating memory instead of using a fixed-size stack buffer. Ensure there are no memory leaks after your fix.
2. Recompile the C extension using the provided `/home/user/app/setup.py` so the changes take effect (build it in-place).
3. The server runs on `ws://localhost:8765`. (You can start it manually in the background by running `python3 /home/user/app/server.py &`).
4. Write a Python testing utility at `/home/user/app/test_client.py` using the `websockets` and `json` modules. The script must:
    - Connect to the server.
    - Send a JSON payload exactly matching this structure: `{"action": "reverse", "text": "<payload>"}` where `<payload>` is a string consisting of exactly 100 uppercase 'Z' characters.
    - Receive the JSON response from the server.
    - Extract the transformed string from the response's `"result"` field.
    - Write *only* the extracted transformed string to a file named `/home/user/test_result.log`.

Requirements:
- Ensure the server does not crash when the 100-character string is sent.
- Ensure the build artifacts are correctly generated in `/home/user/app`.
- The final verification will check the contents of `/home/user/test_result.log` and verify the C extension source code.