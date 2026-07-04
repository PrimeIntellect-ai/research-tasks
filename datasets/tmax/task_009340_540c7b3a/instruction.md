You are tasked with migrating a legacy Python 2 interpreter engine to Python 3 and exposing it over a modern WebSocket interface. 

Currently, there is a Python 2 script located at `/home/user/legacy_logic.py`. This script contains the logic for a custom stack-based Virtual Machine (VM) and a custom `RingStack` data structure. It was designed to parse a custom binary bytecode format, but it relies heavily on Python 2-specific string/bytes handling (like using `ord()` on strings, `cmp()`, and lacking explicit encoding boundaries).

Your objectives are:
1. Set up a Python 3 virtual environment in `/home/user/venv`.
2. Install the `websockets` library in this virtual environment.
3. Rewrite the VM and data structure logic into a new Python 3 compatible file at `/home/user/modern_vm.py`. You must fix all Python 2-isms (e.g., `str` vs `bytes`, `xrange`, `cmp()`, etc.) while preserving the exact mathematical and operational behavior of the VM instructions.
4. In `/home/user/modern_vm.py`, implement an `asyncio`-based WebSocket server using the `websockets` library. 
   - The server must listen on `localhost`, port `8765`.
   - When a client connects and sends a message, the server should expect a **Base64 encoded string**.
   - The server must decode this Base64 string into raw bytes, and feed it to the migrated VM `execute` function.
   - Upon encountering the HALT instruction (or reaching the end of the bytecode), the server must serialize the final state of the `RingStack` (as a JSON array of integers) and send it back to the client over the WebSocket.
   - After sending the response, close the connection.
5. Create a shell script `/home/user/start_server.sh` that activates the virtual environment and starts the `modern_vm.py` server in the background, writing its PID to `/home/user/vm.pid`.

**Bytecode Specification (for your understanding):**
- Instructions are 2 bytes long: `[opcode: 1 byte (unsigned)][operand: 1 byte (signed 8-bit integer)]`.
- Opcodes: 
  - `0x01`: PUSH operand
  - `0x02`: ADD (pops top two elements, adds them, pushes result)
  - `0x03`: MULTIPLY (pops top two elements, multiplies them, pushes result)
  - `0x04`: ROTATE_STACK (pops `a`, rotates the remaining stack right by `a` positions. Handled by a custom `cmp` sort in the legacy code which you must replicate functionally without `cmp`).
  - `0x05`: HALT

Ensure your server correctly processes multiple sequential connections and that the math matches the original exactly.