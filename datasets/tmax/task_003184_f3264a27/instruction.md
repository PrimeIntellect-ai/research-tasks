You are a compliance officer auditing a financial database system for a recent outage caused by a transaction deadlock. 

You have two pieces of evidence:
1. `/app/audit_dashboard.mp4`: A screen recording of the system health dashboard. The screen is normally solid green, but it flashes solid red (RGB: 255, 0, 0) for exactly one frame when the deadlock occurs.
2. `/home/user/tx_log.csv`: A log of database lock actions. 
   Format: `timestamp_sec,tx_id,resource_id,action`
   - `action` can be `ACQUIRE`, `RELEASE`, or `WAIT`.
   - `ACQUIRE`: The transaction successfully locked the resource.
   - `WAIT`: The transaction is blocked waiting for the resource (which is currently ACQUIREd by another transaction).
   - `RELEASE`: The transaction frees the resource.

Your objective:
1. Find the exact timestamp (in seconds, to 2 decimal places) of the red frame in the video.
2. Write a highly optimized C program at `/home/user/deadlock_detector.c` that reads a CSV log and a target timestamp.
   - Usage: `./deadlock_detector <csv_path> <max_timestamp>`
   - The program must parse all events up to and including `<max_timestamp>`.
   - It must build a Wait-For Graph (WFG) where a directed edge exists from Transaction A to Transaction B if A is `WAIT`ing for a resource that B currently holds (`ACQUIRE`d and not yet `RELEASE`d).
   - It must detect the cycle in the graph (the deadlock) and print the involved `tx_id`s as a comma-separated list, sorted in ascending order.
3. Compile your program to `/home/user/deadlock_detector`.
4. Run your program on `/home/user/tx_log.csv` using the timestamp you found in the video. Save the stdout output (just the comma-separated list, e.g., `42,105,302`) to `/home/user/deadlock_result.txt`.

Constraints & Performance Verification:
- You must write the C program using only standard POSIX C libraries. Do not use external libraries (no glib, etc.).
- Your C program will be evaluated on a hidden, massive CSV log (over 5 million rows). It must execute in under 1.5 seconds. Use efficient data structures (e.g., custom hash maps, adjacency lists for recursive graph traversal).