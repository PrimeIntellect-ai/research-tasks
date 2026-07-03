You are a build engineer managing low-level artifacts. The embedded firmware team has sent you an extracted code payload embedded within a structured JSON metadata file. Your goal is to parse this artifact, compile it into a minimal freestanding executable, run it, and report the execution result via a WebSocket test harness.

All your work must be done in the `/home/user` directory.

Here is the exact workflow you need to implement:

1. **Structured Data Parsing & Minimal Program Construction:**
   Read the file `/home/user/artifact.json`. It contains structured metadata and raw x86_64 assembly instructions (Intel syntax) in a JSON format. Write a Python script that parses this JSON file and generates a valid GNU assembly file named `/home/user/payload.s`. The assembly file must expose a `_start` symbol as the entry point and contain the instructions exactly as specified in the JSON.

2. **Build System Configuration:**
   Write a `Makefile` in `/home/user` that assembles `/home/user/payload.s` and links it into a statically linked, freestanding ELF executable named `/home/user/payload_bin`. You must use standard GNU binutils (`as` and `ld`). Do not link against libc.

3. **WebSocket Communication:**
   You will find a WebSocket test harness server script at `/home/user/ws_harness.py`.
   Write a Python script `/home/user/notify.py` that takes the exit code of your built executable as a command-line argument, connects to the WebSocket server running locally at `ws://localhost:8765`, and sends a JSON message with the following exact structure:
   `{"artifact_id": "<id_from_artifact_json>", "exit_code": <integer_exit_code>}`

4. **End-to-End Orchestration:**
   Create a bash script named `/home/user/run_e2e.sh` that automates the entire process:
   - Starts the `/home/user/ws_harness.py` server in the background and waits 1 second for it to bind.
   - Runs your parsing script to generate `payload.s`.
   - Invokes `make` to build `payload_bin`.
   - Executes `./payload_bin` and captures its exit code.
   - Runs your `notify.py` script to send the exit code to the WebSocket server.
   - Gracefully terminates the background WebSocket server.

*Constraints & Hints:*
- Use `pip install websockets` in your scripts or environment if you need the websockets library for Python.
- The `ws_harness.py` script will automatically write a verification file to `/home/user/verification.log` if it receives the correct WebSocket payload. 
- You must ensure the assembly code is valid for `as` (you may need to specify `.intel_syntax noprefix` and `.global _start` at the top of your `.s` file).