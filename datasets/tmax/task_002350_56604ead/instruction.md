You are acting as a systems compliance officer. We are currently auditing our system's access logs and permission graphs. 

Historically, we have used a proprietary, compiled binary called `/app/legacy_audit_tool` to process access logs and generate compliance risk reports. However, for transparency and maintainability, we need to replace this black-box binary with a clear, auditable Python script.

Your task is to write a Python script at `/home/user/audit_processor.py` that perfectly replicates the behavior, logic, and exact output format of `/app/legacy_audit_tool`. 

**Behavior of the Legacy Tool:**
1. It reads a CSV from standard input (`stdin`) with the header: `EventID,Actor,Target,ActionType,SeverityScore`. (SeverityScore is an integer).
2. It filters out any rows where `SeverityScore < 5`.
3. It constructs a bipartite access graph between `Actor`s and `Target`s.
4. For each `Actor`, it computes an analytical aggregation: `ActorRisk` = sum of `SeverityScore` for all actions performed by that actor across all targets.
5. For each `Target`, it computes a `VulnerabilityIndex`, which is the sum of the `ActorRisk` of all *unique* Actors that interacted with that Target.
6. It sorts the `Target`s by `VulnerabilityIndex` descending. In case of a tie, it sorts by `Target` string alphabetically (ascending).
7. It paginates the results, taking exactly the top 10 most vulnerable targets (Page 1 of size 10).
8. It outputs a rigorously formatted JSON schema exactly like this:
   `[{"target": "target_name", "vulnerability_index": 123}, ...]`

**Instructions:**
1. You may execute `/app/legacy_audit_tool` with various mock CSV inputs to observe its exact output formatting (spacing, keys, edge cases). 
2. Write your Python script at `/home/user/audit_processor.py`. It must read from `sys.stdin` and print the resulting JSON to `sys.stdout`.
3. Your script's output must be bit-for-bit identical to the legacy tool for any valid input. Do not include extra logs, debugging text, or print statements.
4. Use standard Python libraries (e.g., `csv`, `json`, `collections`).