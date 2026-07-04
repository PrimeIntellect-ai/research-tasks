You are a Database Reliability Engineer (DRE) managing the backup systems for a highly concurrent distributed database. Recently, concurrent backup processes and user transactions have been deadlocking, causing cascading outages. 

You have two objectives:
1. Parse a corrupted visual dashboard log to recover the historical transaction lock events.
2. Build a C++ deadlock resolution engine that can process a stream of wait-for graph events and deterministically resolve deadlocks based on graph analytics.

**Part 1: Video Extraction**
There is a video file located at `/app/dashboard.mp4` containing a screen recording of the database lock dashboard. Due to a logging failure, this video is the only record of the events leading up to yesterday's crash.
- The video runs at 1 frame per second (1 fps).
- Each frame contains a single lock event written in large black text on a white background in the center of the screen.
- Extract these events in order and save them to `/home/user/historical_events.txt`.

**Part 2: C++ Deadlock Resolution Engine**
Write a C++ program at `/home/user/resolve_deadlocks.cpp` and compile it to `/home/user/resolve_deadlocks`. The program must read a stream of events from `stdin` and print resolutions to `stdout`.

Input Commands (one per line):
- `T <txn_id> <type>`: Registers a transaction. `<txn_id>` is an integer. `<type>` is either `BACKUP` or `USER`.
- `W <txn_id_1> <txn_id_2>`: `<txn_id_1>` waits for `<txn_id_2>`. Adds a directed edge in the wait-for graph.
- `R <txn_id_1> <txn_id_2>`: `<txn_id_1>` stops waiting for `<txn_id_2>`. Removes the directed edge.

Processing Rules:
- Every time a `W` command is processed, check if it creates a directed cycle in the wait-for graph (a deadlock).
- If a cycle is detected, immediately print: `DEADLOCK DETECTED: <node1> <node2> ... <nodeN>` (list the nodes in the cycle, sorted in ascending order, separated by a single space).
- Next, you must select exactly ONE transaction in the cycle to abort to break the deadlock:
  1. **Type Priority**: Always abort a `USER` transaction over a `BACKUP` transaction.
  2. **Graph Analytics (Degree Centrality)**: If there is a tie in type, abort the transaction in the cycle that has the highest out-degree in the *entire* wait-for graph (i.e., the transaction that is waiting on the most other transactions globally).
  3. **ID Tie-breaker**: If there is still a tie, abort the transaction with the highest `<txn_id>`.
- Once the victim is chosen, print: `ABORT: <victim_txn_id>`.
- Remove the victim transaction and ALL of its incoming and outgoing wait edges from the graph.
- If a command references an unregistered `<txn_id>`, ignore it. 

**Part 3: Execution**
Run your compiled C++ engine on the extracted `/home/user/historical_events.txt` and save the output to `/home/user/resolution_log.txt`.

*Note: Your compiled binary `/home/user/resolve_deadlocks` will be rigorously tested against an extensive fuzzing suite to ensure your cycle detection and graph analytical tie-breaking logic is bit-exact equivalent to our reference engine.*