You are a database administrator building a preventative tool to optimize query scheduling and avoid deadlocks in our custom transaction engine. 

We need a C command-line application that acts as a transaction schedule sanitizer. It will read a schedule of interleaved database operations and determine if it will result in a deadlock using a Wait-For Graph.

**Requirements:**

1. **Vendored Library Fix:**
   We are using a third-party C graph library located at `/app/cgraph-1.0`. It contains the source code for building a lightweight directed graph structure. However, the `Makefile` in that directory has a deliberate perturbation (a typo in the build rules) that prevents it from compiling.
   - Fix the `Makefile` in `/app/cgraph-1.0`.
   - Build the library to produce `libcgraph.a`.

2. **Deadlock Detector Implementation:**
   Write a C program at `/home/user/deadlock_detector.c` that compiles to `/home/user/deadlock_detector`. It must link against the fixed `libcgraph.a`.
   Your program must accept a single command-line argument: the path to a transaction schedule file.

   **Schedule File Format:**
   Each line is an operation in the format: `T<id> <ACTION> <RESOURCE>`
   - `id`: An integer transaction ID (e.g., `1`, `2`).
   - `ACTION`: Either `READ` or `WRITE`.
   - `RESOURCE`: A string representing the table or row (e.g., `Users`, `Orders`).
   - Example line: `T1 READ Users`

   **Locking Rules (Strict Two-Phase Locking):**
   - `READ` requests a Shared (S) lock.
   - `WRITE` requests an Exclusive (X) lock.
   - If a transaction requests a lock on a resource that is incompatible with a lock already held by another transaction, the requesting transaction **waits** for the holding transaction(s).
     - S is compatible with S.
     - X is incompatible with S and X.
     - S is incompatible with X.
   - Locks are never released in these snippets (assume they are held until the end of time for the purpose of this analysis).
   - If a transaction is blocked (waiting), any subsequent operations for that transaction in the file are ignored until it is unblocked (which won't happen in these partial schedules).
   - *Graph Traversal / Deadlock Condition:* You must maintain a Wait-For Graph (where a directed edge A -> B means Transaction A is waiting for Transaction B). If adding a wait dependency creates a **cycle** in the graph, a deadlock has occurred.

3. **Validation & Output:**
   - If the schedule processes completely without creating a cycle in the wait-for graph, your program must exit with status code `0`.
   - If a cycle is detected at any point, your program must immediately exit with status code `1`.

Your detector will be tested against two sets of corpora located in `/app/corpora/clean/` and `/app/corpora/evil/`. 
- The `clean` schedules do not contain deadlocks.
- The `evil` schedules contain deadlocks.
Your executable must correctly classify 100% of the files.