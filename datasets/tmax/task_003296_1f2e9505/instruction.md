You are an AI assistant helping a compliance officer build an automated auditing tool. We need to trace user and group access permissions across our internal systems to ensure no unauthorized access pathways exist. 

The environment uses a multi-service architecture containing an access graph database and a fast-access override cache.

**System Architecture & Services:**
There is a startup script located at `/app/start_services.sh` which brings up the following background services:
1. **PostgreSQL (Port 5432)**: Stores the hierarchical access graph. 
   - Credentials: User: `auditor`, Password: `audit123`, Database: `compliance`.
   - Table `access_edges`: Columns `source_id` (VARCHAR), `target_id` (VARCHAR). This represents a directed edge indicating access or membership (e.g., UserA -> GroupB, or GroupB -> ResourceC).
2. **Redis (Port 6379)**: Stores temporary direct access overrides. No password.

**Your Task:**
Write a Go CLI program `/home/user/audit.go` and compile it to an executable at `/home/user/audit`. 

The program must take exactly two command-line arguments: `source_node` and `target_node`.
Execution format: `./audit <source_node> <target_node>`

**Logic Rules:**
1. **Check Overrides:** First, check Redis for a key named exactly `override:<source_node>:<target_node>`.
   - If the value is `"ALLOW"`, immediately output `{"status":"ALLOW","path":["<source_node>","<target_node>"],"reason":"redis_override"}`
   - If the value is `"DENY"`, immediately output `{"status":"DENY","path":[],"reason":"redis_override"}`
2. **Graph Traversal:** If the Redis key does not exist, query PostgreSQL to find the **shortest directed path** from `source_node` to `target_node` using the `access_edges` table.
   - If a path is found, output `{"status":"ALLOW","path":["<source_node>","...","<target_node>"],"reason":"graph_path"}`
   - If multiple paths tie for the shortest length, select the path that is **lexicographically smallest** (compare the sequence of node IDs from start to finish).
   - If no path exists, output `{"status":"DENY","path":[],"reason":"no_path"}`

**Output Requirements:**
- The output MUST be a single line of valid, unformatted JSON exactly matching the schemas described above. 
- Print the output to `stdout`. Do not print any extraneous logs to `stdout` (you may use `stderr` for debugging).

**Environment Setup:**
Before testing your code, be sure to run `/app/start_services.sh` to initialize the database and cache. You are encouraged to inspect the schema and insert mock data while developing.