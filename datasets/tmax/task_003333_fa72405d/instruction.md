You are tasked with setting up a polyglot build system and translating a mathematical algorithm to Python for a mock WebSocket data feed.

You have been provided a working directory at `/home/user/build_env`. This directory contains the beginnings of a C project that calculates the Collatz sequence length, but the build system is broken and the backend needs a Python equivalent for the WebSocket server.

Your tasks are to:
1. **Repair the Makefile**: The `Makefile` in `/home/user/build_env` is broken. Fix it so that running `make` successfully compiles `algo.c` into an executable named `collatz`. (Note: Ensure the executable runs correctly and uses standard Makefile syntax).
2. **Translate Code**: Translate the mathematical logic found in `algo.c` into a Python script named `/home/user/build_env/ws_handler.py`. The Python function must take an integer `N` and return the number of steps to reach 1 using the exact same rules as the C program.
3. **Design Custom Payload**: Your Python script (`ws_handler.py`) must calculate the Collatz sequence length for the initial value `N = 837799`. 
4. **Mock WebSocket Communication**: Instead of sending over a live WebSocket, your Python script must package the result into a custom JSON data structure and write it to `/home/user/build_env/ws_payload.json`. 

The JSON payload strictly must follow this schema:
```json
{
  "channel": "math_ws",
  "message": {
    "type": "collatz_len",
    "start_val": 837799,
    "steps": <calculated_integer_steps>
  }
}
```

Ensure the C code is successfully compiled via `make` and your Python script generates the exact required JSON file.