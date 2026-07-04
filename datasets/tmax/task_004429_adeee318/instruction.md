You are a database administrator tasked with optimizing queries and resolving deadlocks. A recent spike in database errors has been traced to transaction deadlocks, and you need to build a tool to analyze the transaction wait-graph and identify the most immediate deadlock (the shortest cycle).

You have been provided a CSV file at `/home/user/waits_for.csv` representing the "waits-for" graph of active transactions. 
The CSV has two columns: `waiter_tx` and `holder_tx`. Each row indicates that transaction `waiter_tx` is waiting for a lock held by transaction `holder_tx`. This represents a directed edge from `waiter_tx` to `holder_tx`.

Your task is to:
1. Write a C++ program at `/home/user/solve.cpp` that reads `/home/user/waits_for.csv`.
2. Materialize the data into a directed graph in memory.
3. Detect the shortest cycle in the graph (which represents the smallest deadlock involving the fewest transactions).
4. If there are multiple cycles of the same shortest length, select the cycle that contains the numerically smallest transaction ID among all such cycles.
5. Export the transaction IDs involved in this chosen shortest cycle as a JSON array of integers, sorted in strictly ascending order, to the file `/home/user/deadlock.json`.

Compile your C++ code and run it to produce the output file. You may use standard C++ libraries (C++17 is available). 

For example, if the shortest cycle involves transactions 45, 12, and 33, the contents of `/home/user/deadlock.json` must be exactly:
```json
[12, 33, 45]
```
Ensure your formatting matches this style exactly (brackets, comma-separated, optional spaces after commas).