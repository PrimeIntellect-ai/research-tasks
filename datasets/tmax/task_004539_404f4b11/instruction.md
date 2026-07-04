You are a Database Administrator investigating a recurring deadlock issue in a distributed database system. You need to build a C++ tool that reconstructs the database's internal transaction wait-for graph from a relational lock log, detects cycles (deadlocks), and outputs a validated JSON schema of the conflicting transactions.

Your objective is to write a C++ program that reads `/home/user/tx_locks.csv`, builds a dependency graph, detects all simple cycles, and outputs the result to `/home/user/deadlock_report.json`.

**Data Reverse Engineering & Graph Projection Rules:**
1. The input file `/home/user/tx_locks.csv` contains logs with the following columns: `timestamp,tx_id,resource_id,status`.
2. `status` is either `GRANTED` (the transaction currently holds the lock on the resource) or `WAITING` (the transaction is blocked waiting for a lock on the resource).
3. **Wait-For Graph Construction:** A directed edge exists from Transaction A to Transaction B (i.e., A -> B) if Transaction A is `WAITING` for a `resource_id` that is currently `GRANTED` to Transaction B.

**Cycle Detection & Output Constraints:**
1. Find all elementary cycles in the Wait-For Graph.
2. Output a strictly formatted JSON file to `/home/user/deadlock_report.json`.
3. The JSON must match this exact schema structure:
```json
{
  "deadlocks": [
    ["T1", "T2", "T3"],
    ["T4", "T5"]
  ]
}
```
4. **Ordering rules for deterministic output:** 
   - Within each cycle's array, sort the transaction IDs alphabetically (e.g., `["T1", "T2", "T3"]` instead of `["T2", "T3", "T1"]`).
   - Sort the outer `deadlocks` array based on the first element of each cycle's array alphabetically.

**Requirements:**
- Write your solution in a file named `/home/user/deadlock_analyzer.cpp`.
- Compile it using `g++ -std=c++17 /home/user/deadlock_analyzer.cpp -o /home/user/deadlock_analyzer`.
- Execute your binary so that it reads the CSV and produces `/home/user/deadlock_report.json`.
- Use only standard bash/coreutils and the C++ standard library. Do not use external C++ libraries like nlohmann/json or boost; construct the simple JSON output manually using standard strings or streams.