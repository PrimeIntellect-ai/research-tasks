You are acting as a Compliance Officer performing a system audit. We are transitioning from a legacy compiled access-control auditor to a modern Python-based compliance pipeline. 

Your objective is to reverse-engineer a stripped, legacy binary oracle and recreate its exact behavior in Python. The legacy binary is located at `/app/audit_bin`.

**Context:**
The `/app/audit_bin` program reads a JSON array of audit operations from standard input (stdin), processes them (performing schema validation, NoSQL-style aggregation, and graph materialization internally), and outputs a strict JSON object to standard output (stdout) representing user risk scores. 

We don't have the source code for the legacy binary, but we know it processes the following types of operations in the JSON array:
1. `{"op": "add_node", "node": <string>, "is_sensitive": <boolean>}` - Registers a resource node in the system.
2. `{"op": "add_edge", "src": <string>, "dst": <string>}` - Creates a directional hierarchy between resources.
3. `{"op": "grant", "user": <string>, "node": <string>}` - Grants a user direct access to a node.

**Your Tasks:**
1. Interact with `/app/audit_bin` by passing various JSON payloads to its stdin to deduce the exact graph projection logic and how "risk scores" are aggregated per user.
2. Create a Python script at `/home/user/auditor.py`.
3. Your script must read a JSON array from `sys.stdin`, parse the schema, perform the exact same graph materialization and risk aggregation pipeline, and print the resulting JSON to `sys.stdout`.
4. The output must be BIT-EXACT equivalent to the output of `/app/audit_bin` for any valid input sequence. Ensure your output schema, key ordering, and whitespace matches the binary's output precisely (the binary outputs tightly packed JSON with sorted keys).

*Note: You have standard reverse-engineering tools (strings, objdump) available, but treating the binary as a black-box oracle by feeding it crafted inputs is likely the fastest way to deduce the compliance logic.*