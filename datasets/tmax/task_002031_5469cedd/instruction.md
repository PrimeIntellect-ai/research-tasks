You are helping a database researcher organize and analyze a dataset of concurrent transactions. The researcher has dumped a graph representation of the database's lock table, and needs to detect if there is a deadlock (a cycle in the "WAIT_FOR" relationships).

The raw graph export is located at `/home/user/transactions.graph` and contains mixed edge types separated by spaces:
```text
TxA :ACQUIRED Lock1
TxB :ACQUIRED Lock2
TxA :WAIT_FOR TxB
TxB :WAIT_FOR TxC
TxC :WAIT_FOR TxA
TxD :WAIT_FOR TxE
```

Your task is to build a two-part pipeline:
1. Write a C++ program `/home/user/deadlock_detector.cpp` that reads a list of directed edges from standard input (one edge per line, format: `SourceNode,TargetNode`). It should build a directed graph and find all nodes that are part of a cycle (a deadlock). 
2. Write a bash script `/home/user/process.sh` that chains everything together. It must:
   - Extract only the `:WAIT_FOR` edges from `/home/user/transactions.graph` using standard shell tools (like `grep` or `awk`).
   - Format them as `SourceNode,TargetNode` (e.g., `TxA,TxB`).
   - Pipe this data into your compiled C++ program.
   - Save the standard output of the C++ program to `/home/user/deadlock_report.json`.

**Output Schema Requirements:**
The C++ program must validate and output its results in strictly formatted JSON to standard output. The JSON must exactly match this schema:
```json
{
  "deadlock_detected": true,
  "deadlocked_transactions": ["TxA", "TxB", "TxC"]
}
```
*Note: The `deadlocked_transactions` array must contain the names of all nodes involved in ANY cycle, sorted lexicographically. If no deadlocks exist, `deadlock_detected` should be `false` and the array should be empty `[]`.*

**Execution:**
Ensure your C++ file is compiled to `/home/user/detector` and that `/home/user/process.sh` is executable and successfully generates `/home/user/deadlock_report.json` when run.