You are a mobile build engineer tasked with maintaining our CI/CD pipelines. Recently, we suspect that a malicious actor has been tampering with our build pipeline configurations. They have injected obfuscated "security check" expressions into the build dependency graph.

To safely analyze these expressions without executing potentially malicious bash code directly, you need to write a Python script that parses the dependency graph, safely evaluates the injected expressions using a custom emulator, and reports the sequence of results to our local monitoring dashboard via WebSockets.

Here are the requirements:

1. The build pipeline is defined in `/home/user/pipeline.json`. It contains a JSON object where each key is a build step ID, and the value is an object with two properties:
   - `deps`: A list of step IDs that must be completed before this step.
   - `expr`: A string containing the obfuscated expression in Prefix (Polish) notation.

2. Write a Python script at `/home/user/analyze.py` that:
   - Reads and parses `/home/user/pipeline.json`.
   - Performs a topological sort on the build steps. If multiple steps are available to be processed, process them in alphabetical order of their step IDs to ensure deterministic execution.
   - For each step (in the strict topologically sorted order), evaluate its `expr`.
   - The expression language is a simple integer arithmetic language in Prefix notation. It supports the following operators: `ADD`, `SUB`, `MUL`, `DIV` (integer division), and `XOR` (bitwise XOR). All operands are integers. For example, `ADD XOR 10 5 3` evaluates to `((10 XOR 5) + 3)` = 18.

3. As your script evaluates each step, it must send a JSON payload over a WebSocket connection to `ws://localhost:9999`.
   - The payload format must be: `{"step": "<step_id>", "result": <integer_result>}`
   - You must send these messages one by one in the exact topologically sorted order.
   - Wait for the WebSocket connection to cleanly close after sending all messages.

4. A WebSocket server is already running on `ws://localhost:9999` to receive your payloads. You may need to install the `websockets` Python package if you choose to use it.

Run your script to complete the analysis. The local server will automatically log the received payloads, which will be used to verify your work.