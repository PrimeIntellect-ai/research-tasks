You are an integration developer tasked with creating a tool to test a legacy API endpoint. The API does not accept JSON or XML; instead, it accepts a custom binary payload that acts as bytecode for a small virtual machine on the server.

You have a test definition in JSON format located at `/home/user/api_test.json`. Your goal is to write a Python script at `/home/user/process_api.py` that translates this JSON sequence of pseudo-code instructions into the precise binary bytecode (serialization and code translation) and then acts as a local emulator to execute that bytecode to determine the expected result.

Here is the specification for the bytecode format and the emulator:

**Opcodes (1 byte each):**
- `PUSH` = `0x01`. Pushes a 2-byte unsigned little-endian integer onto the stack. The integer immediately follows the opcode in the binary stream.
- `ADD` = `0x02`. Pops the top two values from the stack, adds them, and pushes the result.
- `SUB` = `0x03`. Pops the top value (B) and the next value (A) from the stack, computes `A - B`, and pushes the result.
- `MUL` = `0x04`. Pops the top two values from the stack, multiplies them, and pushes the result.

Your script `/home/user/process_api.py` must perform the following actions:
1. Parse the `/home/user/api_test.json` file. It contains a single JSON object with an "instructions" array of strings (e.g., `["PUSH 50", "PUSH 10", "SUB"]`).
2. Translate these instructions into the described binary bytecode format.
3. Save the resulting binary payload exactly to `/home/user/api_payload.bin`.
4. Read `/home/user/api_payload.bin` and emulate the stack machine's execution.
5. Write the final integer remaining on the stack (as a plain text string) to `/home/user/final_state.txt`.

Assume all stack operations are valid and will not result in underflows or overflows requiring special handling outside standard Python arithmetic.

Once your script is ready, execute it to generate `/home/user/api_payload.bin` and `/home/user/final_state.txt`.