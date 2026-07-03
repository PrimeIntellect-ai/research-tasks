You are a data analyst investigating severe database deadlock issues. You have two objectives: analyzing a monitoring video for error flags, and building a C++ tool to detect deadlocks from transaction CSV logs.

**Part 1: Video Analysis**
A system monitoring dashboard was recorded during an outage. The video is located at `/app/dashboard_recording.mp4`. 
Whenever the system registered a critical lock contention, the screen flashed solid red (`#FF0000`).
Use `ffmpeg` or any suitable tool to analyze this video and count the exact number of frames that are completely, solidly red. 
Write this integer count to `/home/user/red_frame_count.txt`.

**Part 2: Deadlock Detector (C++)**
You need to build a C++ CLI tool that parses transaction log CSVs to detect deadlocks (cycles in the wait-for graph).
The transaction logs are formatted with the following header:
`timestamp,tx_id,action,resource_id`

*   `tx_id` and `resource_id` are alphanumeric strings.
*   `action` is either `HOLD` (the transaction currently holds the lock on the resource) or `WAIT` (the transaction is waiting to acquire a lock on the resource).

A transaction $A$ waits for transaction $B$ if $A$ is in the `WAIT` state for a `resource_id` that $B$ currently has in the `HOLD` state. A deadlock occurs if there is a cycle in these dependencies (e.g., $A$ waits for $B$, $B$ waits for $C$, $C$ waits for $A$).

Create a C++ source file at `/home/user/detector.cpp` and compile it to an executable at `/home/user/detector`.
Your executable must accept a single command-line argument: the path to a CSV file.
Example: `/home/user/detector /path/to/log.csv`

Requirements for `/home/user/detector`:
1.  Read the specified CSV file.
2.  Project the data into a wait-for graph.
3.  Use a recursive cycle-detection algorithm to determine if a deadlock exists.
4.  If a deadlock cycle exists in the graph, print exactly `REJECT` to standard output.
5.  If no deadlock cycle exists, print exactly `ACCEPT` to standard output.
6.  The program must exit with status code 0 in both cases.

Your program will be tested against two corpora of CSV logs: an "evil" directory containing deadlocks, and a "clean" directory containing safe transactions. You must achieve 100% accuracy on both.