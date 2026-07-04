You are a compliance officer automating an audit of a system's access logs. You suspect that users are exploiting a vulnerability to assume roles they shouldn't have access to, typically following a burst of failed attempts.

You have an SQLite database at `/home/user/compliance.db` containing three tables:
1. `users`:
   - `user_id` (TEXT)
   - `base_role` (TEXT)
2. `role_graph`:
   - `parent_role` (TEXT)
   - `child_role` (TEXT)
   *(A user with a `base_role` can legitimately assume any role that is reachable via a directed path from their `base_role` in this graph, including the base role itself. For example, if A->B and B->C, a user with base role A can assume A, B, or C).*
3. `events`:
   - `event_id` (INTEGER)
   - `timestamp` (INTEGER)
   - `user_id` (TEXT)
   - `role_assumed` (TEXT)
   - `status` (TEXT: 'SUCCESS' or 'FAILURE')

Your task is to write a Rust application in `/home/user/auditor` that processes this database to find "Suspicious Escalations". 

An event is defined as a Suspicious Escalation if ALL the following are true:
1. The event `status` is `'SUCCESS'`.
2. Within the 5 events immediately preceding this event for that **same user** (ordered by `timestamp`), there are 3 or more events with a `'FAILURE'` status. You must compute this using an SQL Window Function in your query.
3. The `role_assumed` is **unreachable** from the user's `base_role` according to the `role_graph` (you must materialize the graph in Rust and evaluate reachability).

The application must output the top 10 most recent Suspicious Escalations (sorted by `timestamp` DESC).

Write the results to `/home/user/flagged_events.json` as a JSON array of objects with exactly this format:
```json
[
  {
    "event_id": 105,
    "user_id": "u1",
    "role_assumed": "admin"
  }
]
```

Requirements:
- Initialize your Rust project at `/home/user/auditor`.
- You may use the `rusqlite`, `serde`, and `serde_json` crates.
- Produce the exact JSON file specified at `/home/user/flagged_events.json`.