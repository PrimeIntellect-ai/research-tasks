As a compliance officer, I need to audit our system's access delegation logs. We have a problem where employees are delegating system permissions to each other in cycles, which has led to distributed deadlocks during concurrent transaction processing. 

Your task is to analyze our employee database and delegation logs to identify the most critical bottlenecks (using centrality) and locate specific deadlock risks (cycles).

The data is split across two formats:
1. A relational SQLite database at `/home/user/employees.db`. It contains a table `employees` with columns `emp_id` (TEXT) and `department` (TEXT).
2. A document-based JSON Lines file at `/home/user/delegations.jsonl`. Each line is a JSON object representing a permission delegation, with keys `from_emp` and `to_emp`.

You need to write and execute a Python script that performs the following:
1. **Cross-Representation Mapping**: Read both data sources. You must only consider delegations where BOTH the `from_emp` and `to_emp` exist in the `employees.db` database. Ignore any delegations involving unknown IDs.
2. **Graph Projection**: Construct a directed graph where nodes are `emp_id`s and edges represent a delegation from `from_emp` to `to_emp`.
3. **Graph Analytics**:
   - Calculate the PageRank centrality for all nodes in this valid graph (use standard PageRank with alpha=0.85).
   - Find all simple cycles (directed cycles) of length exactly 3. These represent our 3-way deadlocks.

**Output Requirements:**
Create a JSON file at `/home/user/deadlock_audit.json` with the following exact structure:
```json
{
  "top_bottlenecks": [
    "emp_id_with_highest_pagerank",
    "emp_id_with_second_highest_pagerank",
    "emp_id_with_third_highest_pagerank"
  ],
  "deadlock_cycles": [
    ["E_A", "E_B", "E_C"],
    ["E_X", "E_Y", "E_Z"]
  ]
}
```

**Constraints for `deadlock_cycles`:**
- Each cycle must be a list of 3 employee IDs.
- Within each cycle's list, rotate the elements so that the lexicographically smallest `emp_id` is first. (e.g., if the cycle is E3->E1->E2, write it as `["E1", "E2", "E3"]`).
- Sort the outer list of `deadlock_cycles` lexicographically by the first element, then second, then third.

You may install any Python packages you need (like `networkx` or `pandas`) using pip.