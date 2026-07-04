You are a build engineer managing a CI/CD pipeline. We have a legacy binary artifact generator that we need to integrate into our modern web-based artifact processing pipeline. We lost the source code for the legacy tool, but we know how its output should be interpreted.

Your task is to write a Python service that acts as an integration webhook. This service will invoke the legacy binary, parse its output (a custom compiled bytecode), emulate the execution of that bytecode to calculate a numerical checksum, and return the result.

Here is the exact specification of what you need to build:

1. **The Web Service:**
   - Create a Python HTTP web server listening exactly on `127.0.0.1:9090`.
   - It must expose a `POST` endpoint at `/process_artifact`.
   - The endpoint must require an authorization header exactly matching: `X-CI-Token: build-eng-2024`. If missing or incorrect, return a 401 status code.
   - The endpoint will receive a JSON payload: `{"artifact_id": <integer>}`.

2. **The Legacy Binary:**
   - A stripped binary is located at `/app/legacy_bytecode_gen`.
   - Your service must execute this binary, passing the `artifact_id` as the only command-line argument: `/app/legacy_bytecode_gen <artifact_id>`.
   - When run, the binary writes a file named `output.bin` in the current working directory. This file contains a custom stream of bytecode.

3. **The Bytecode Emulator:**
   - You must write a parser and emulator for this bytecode.
   - The virtual machine has two 8-bit unsigned integer registers: `reg[0]` and `reg[1]`. Both are initialized to `0` at the start of execution.
   - All arithmetic operations are modulo 256 (standard 8-bit unsigned wrapping).
   - Instructions are exactly 3 bytes long. The first byte is the Opcode. The second and third bytes are Operands.
   - **Instruction Set:**
     * `0x01` (LOAD_CONST): Byte 2 is the 8-bit value. Byte 3 is the register index (0 or 1). Operation: `reg[idx] = value`.
     * `0x02` (ADD): Byte 2 is the source register index. Byte 3 is the destination register index. Operation: `reg[dst] = (reg[dst] + reg[src]) % 256`.
     * `0x03` (MUL): Byte 2 is the source register index. Byte 3 is the destination register index. Operation: `reg[dst] = (reg[dst] * reg[src]) % 256`.
     * `0x04` (XOR_CONST): Byte 2 is the 8-bit value. Byte 3 is the register index. Operation: `reg[idx] = reg[idx] ^ value`.
     * `0xFF` (RETURN): Operands are ignored. Execution halts immediately. The final value of `reg[1]` is the result.

4. **Integration:**
   - Read and execute the instructions from `output.bin` in order until the `RETURN` opcode is reached.
   - Your endpoint must return a 200 OK JSON response containing the final value of `reg[1]`: `{"checksum": <result>}`.
   - Make sure your service stays running in the foreground or background so it can be tested. Put your server code in `/home/user/server.py` and run it.

Please implement the full server and emulator.