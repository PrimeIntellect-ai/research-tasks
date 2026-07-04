` block, and detail the verification criteria, corpus paths, and package state in the `<truth>` block.

<task>
You are acting as a system administrator and capacity planner. We have a locally vendored log aggregation package that is currently broken, and we need to deploy it alongside a robust log sanitizer to process resource usage data.

**Objective 1: Fix the Vendored Package**
A third-party capacity planning package is vendored at `/app/vendor/cap-plan-tools-1.0.0/`. The main entry point is `/app/vendor/cap-plan-tools-1.0.0/aggregator.py`. 
Currently, the package is broken because it is hardcoded to read its configuration and write its internal state to a root-owned directory, causing a `PermissionError` when run as a standard user. 
- Identify the hardcoded privileged path in `aggregator.py`.
- Patch the script so that instead of using the hardcoded path, it defaults to checking the environment variable `CAP_PLAN_DIR`, falling back to `/home/user/cap_plan` if the variable is not set. 

**Objective 2: Create a Log Sanitizer (Adversarial Filter)**
Our capacity monitoring agents send resource usage logs in JSON Lines (JSONL) format. However, the data stream is occasionally corrupted with malformed entries or malicious payloads masquerading as process names.
Create a Python script at `/home/user/sanitize.py` that reads JSONL logs from standard input and prints sanitized JSONL logs to standard output.
Your script must implement the following filtering rules. A line MUST be silently dropped (rejected) if:
1. It is not valid JSON.
2. The `cpu_percent` field is missing, strictly less than 0, or strictly greater than 100.
3. The `memory_mb` field is missing or strictly less than 0.
4. The `process_name` field contains any shell metacharacters (specifically: `;`, `&`, `|`, `<`, `>`).

Valid lines that do not violate any of the above rules must be printed exactly as parsed (or structurally identical) to standard output. 

**Objective 3: Final Integration**
Create the directory `/home/user/cap_plan/logs/`. We will run automated tests against your `/home/user/sanitize.py` script to ensure it correctly preserves clean logs while perfectly rejecting malicious or malformed logs. 
Make sure your Python script is executable (`chmod +x /home/user/sanitize.py`) and uses standard input/output.