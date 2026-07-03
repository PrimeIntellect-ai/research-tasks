You are tasked with building the core orchestrator for a distributed, polyglot build system. This orchestrator must interpret a custom Build-Domain Specific Language (BuildDSL), solve constraint satisfaction problems to assign build steps to appropriate remote workers based on their capabilities, and manage the execution over WebSockets.

Your goal is to write a Python script at `/home/user/build_server.py` that acts as the orchestrator.

Here are the specific requirements:

**1. WebSocket Server Communication:**
- Your script must start a WebSocket server listening on `localhost:9000`.
- It will receive JSON messages from connected clients.
- The first message received will be a worker capability matrix:
  `{"type": "workers", "data": {"worker_name": ["tool1", "tool2"], ...}}`
- The second message will be the build definition written in BuildDSL:
  `{"type": "dsl", "script": "<string>"}`

**2. BuildDSL Interpreter:**
You must write an interpreter to parse the BuildDSL script. The language is line-based and consists of target blocks.
Syntax rules:
- `TARGET <name>` : Starts a new build target block.
- `REQUIRES <tool>` : Specifies a required toolchain. Can appear multiple times per block.
- `AFTER <target_name>` : Specifies a dependency. This target cannot start until `<target_name>` finishes. Can appear multiple times per block.
- `END` : Closes the current target block.
- Empty lines or lines not matching the above should be ignored.

**3. Constraint Satisfaction (Task Assignment):**
- A target can only be assigned to a worker that possesses *all* the tools listed in the target's `REQUIRES` lines.
- If multiple workers satisfy a target's requirements, assign it to the worker whose name is lexicographically smallest (e.g., choose `agent-alpha` over `agent-beta`).
- If a target cannot be assigned to any worker, the build should fail immediately (drop the WebSocket connection and exit).

**4. Build Emulator (Execution):**
- You must simulate the execution of the build graph.
- Send a JSON execution command over the WebSocket for each target:
  `{"type": "execute", "task": "<target_name>", "worker": "<worker_name>"}`
- Targets must only be executed after all their `AFTER` dependencies are completed.
- If multiple targets are ready to execute at the same time, dispatch the one whose target name is lexicographically smallest first.
- Wait for the client to reply with `{"type": "completed", "task": "<target_name>"}` before considering that target finished and dispatching its dependents.
- Once all targets have successfully completed, your server must send `{"type": "done"}` and gracefully shut down.

**5. Logging:**
- Throughout the execution, maintain a log of exactly which task was assigned to which worker.
- Right before your script exits (after sending the "done" message), it must write a JSON file to `/home/user/build_schedule.json`.
- The file must contain a single JSON array of objects representing the exact dispatch order, e.g.:
  `[{"task": "bootstrap", "worker": "worker-1"}, {"task": "compile", "worker": "worker-2"}]`

You can use standard Python libraries, `websockets`, and `asyncio`. You may install necessary dependencies using `pip`. You must run your server so it's ready to accept connections. Do not write the client logic; an automated test will connect to your server acting as the worker network.