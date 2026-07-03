You are a systems programmer debugging a complex C library linking issue in a distributed build environment. The build orchestrator is currently failing to link the final executable due to unresolved symbols and strict version dependencies. 

To debug and resolve this, the build orchestrator has been configured to stream linker errors and dependency constraints over a local WebSocket server. Your task is to write a Python client that connects to this server, parses the proprietary build log stream, evaluates the version constraints against the available compiled libraries on the filesystem, and outputs a final linker resolution file.

Here is the setup:
1. Available shared libraries are located in `/home/user/libs/`. They are named in the format `lib<name>.so.<major>.<minor>.<patch>` (e.g., `libnet.so.1.2.4`).
2. The orchestrator streams build logs via a WebSocket server at `ws://localhost:8080`. (You must start the server by running `python3 /home/user/build_server.py &` before running your client).
3. The stream sends messages line-by-line. You must build a state machine to parse this stream. The stream format follows this structure:
   - `[START BUILD] <target_name>`
   - `[ANALYZE] <module_name>`
   - `[DEPENDENCY] <expression>` (zero or more per module)
   - `[END BUILD]`
4. The `<expression>` in the `[DEPENDENCY]` logs uses a custom format combining logical operators and version constraints. Examples:
   - `libcore >= 1.0.0 AND libcore < 2.0.0`
   - `libnet == 1.2.4 OR libnet >= 1.3.0`
   - `libmath > 3.0.0`
5. Your Python script (`/home/user/solver.py`) must:
   - Connect to `ws://localhost:8080`.
   - Parse the stream using a state machine.
   - For every `[DEPENDENCY]` constraint, parse the expression, compare it against the available versions in `/home/user/libs/`, and select the **highest** version that satisfies the entire expression. (Standard semantic versioning rules apply).
   - If multiple `[DEPENDENCY]` lines target the same library across the build, all constraints for that library must be satisfied simultaneously.
   - Write the absolute paths of the selected libraries to `/home/user/linker_flags.txt`, one per line, sorted alphabetically by library name.

Ensure your Python client gracefully closes the WebSocket connection after receiving the `[END BUILD]` message and writing the output file. You may install any necessary Python packages (like `websockets` or `semantic_version`) to assist you.

Output format for `/home/user/linker_flags.txt`:
```
/home/user/libs/libcore.so.1.2.0
/home/user/libs/libmath.so.3.1.4
...
```