You are acting as a technical assistant to a compliance officer. We are auditing financial transaction records to detect "wash trading" and circular money laundering networks. 

You need to create a C++ tool that analyzes a set of transactions and flags if a circular fund flow (a directed cycle, e.g., Account A -> Account B -> Account C -> Account A) exists.

Here is your environment and requirements:
1. **Adversarial Corpus**: We have transaction logs in JSON format. 
   - Clean logs (no cycles, strictly DAGs/trees) are in `/app/corpus/clean/`.
   - Evil logs (contain at least one circular money flow) are in `/app/corpus/evil/`.
   Your C++ program must output exactly `EVIL` (followed by a newline) if a cycle is detected, and `CLEAN` (followed by a newline) if no cycle exists.

2. **Implementation Constraints (SQL & Graph Pattern Matching)**:
   You must implement the cycle detection using **SQLite3** in-memory databases and **Recursive CTEs**. 
   Your C++ program (`/home/user/audit_checker.cpp`) should:
   - Parse the input JSON file (which contains an array of transaction objects: `[{"tx_id": 1, "src": "acc1", "dst": "acc2", "amount": 150.0}, ...]`).
   - Create an in-memory SQLite database (`:memory:`).
   - Create a table, insert the parsed transaction edges using parameterized queries.
   - Execute a complex recursive CTE to detect if any path loops back to a previously visited `src` account.
   - Print `EVIL` or `CLEAN` to standard output.

3. **Vendored Package**:
   The SQLite3 source code (amalgamation) is vendored at `/app/vendor/sqlite3/`. 
   A starter Makefile is located at `/home/user/Makefile`, but it contains deliberate perturbations (missing linker flags and a broken include path) that prevent compiling SQLite correctly on Linux. You must fix the Makefile to successfully compile your executable to `/home/user/audit_checker`.
   *(Note: You may use standard C++ string manipulation or a lightweight parser for the JSON, as the format is strictly uniform without nested whitespaces).*

**Execution**:
Your final compiled executable must be at `/home/user/audit_checker`. It will be invoked by our automated test suite as:
`./audit_checker /path/to/transactions.json`

Fix the Makefile, write the C++ code, ensure it uses a recursive CTE for graph pattern matching, and successfully classify the provided corpora.