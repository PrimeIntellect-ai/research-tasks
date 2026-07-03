You are a data analyst investigating a database performance incident. The system experienced massive slowdowns, and the DBA team exported a snapshot of active lock contentions into a CSV file. You suspect that multiple distributed deadlocks (circular wait conditions) occurred.

You have been provided with a CSV file at `/home/user/waits_for.csv`. 
The file contains the following columns:
- `waiter_id` (integer): The ID of the process requesting a lock.
- `holder_id` (integer): The ID of the process currently holding the requested lock.
- `wait_start_time` (integer): The Unix timestamp when the wait began.

Your task is to write and execute a Python script that analyzes this CSV file to identify and report all deadlocks. 

A deadlock is defined as a simple cycle in the "wait-for" graph (e.g., Process A waits for B, B waits for C, and C waits for A).

You must generate a JSON file at `/home/user/deadlocks.json` containing a list of all identified deadlocks, adhering to the following strict formatting and sorting rules:
1. Each deadlock should be represented as a JSON array of process IDs in the exact order of the wait cycle.
2. To ensure consistent representation, "rotate" each cycle's array so that it starts with the numerically smallest process ID in that cycle. For example, if the cycle is A -> B -> C -> A, and A is the smallest ID, represent it as `[A, B, C]`. Do not sort the elements inside the cycle (except to determine the starting point), as that would destroy the actual path of the cycle.
3. Determine the "formation time" of each deadlock. The formation time is the maximum `wait_start_time` of all the edges that make up that specific cycle (since the deadlock only materialized when the final wait began).
4. Sort the top-level list of deadlocks chronologically by their formation time in ascending order. If two deadlocks formed at the exact same time, break the tie by sorting them based on their starting process ID in ascending order.

The output must be written to `/home/user/deadlocks.json`.