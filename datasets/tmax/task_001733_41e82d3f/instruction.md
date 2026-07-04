You are assisting a compliance officer auditing an internal database system. We suspect a rogue trader is intentionally crafting concurrent transactions to induce deadlocks and bypass our accounting triggers. 

You need to perform two main tasks:

**Part 1: Video Analysis of the Monitoring Dashboard**
We have a recording of the database performance dashboard located at `/app/deadlock_dashboard.mp4`. Whenever a deadlock occurs in the system, the dashboard flashes a completely solid red frame (RGB: 255, 0, 0). 
Use `ffmpeg` to analyze the video and extract the exact frame numbers where these red flashes occur. 
Save these frame numbers as a comma-separated list in `/home/user/deadlock_frames.txt`.

**Part 2: Deadlock Graph Detector (Go)**
We have exported transaction lock requests from the database into JSON format. We need a Go-based detector to analyze these wait-for graphs and classify them.
Write a Go program at `/home/user/detector.go` that takes a directory path as its single command-line argument.
The program must:
1. Iterate through all `.json` files in the provided directory in alphabetical order.
2. Parse the JSON schema. Each file has the following format:
   ```json
   {
     "transactions": [
       {"id": "T1", "holds_locks_on": ["TableA"], "waiting_for_locks_on": ["TableB"]},
       {"id": "T2", "holds_locks_on": ["TableB"], "waiting_for_locks_on": ["TableA"]}
     ]
   }
   ```
3. Build a directed wait-for knowledge graph (e.g., T1 is waiting for T2 because T2 holds the lock on TableB, which T1 is waiting for).
4. Perform cycle detection. A file is considered "malicious" if its wait-for graph contains at least one cycle (deadlock).
5. For every malicious file detected, print ONLY the file name (e.g., `attack_1.json`) to standard output, each on a new line. Do not print anything for clean files.

You have access to a clean corpus and an evil corpus for testing:
- Clean corpus: `/app/corpus/clean/` (High concurrency, but no wait-for cycles)
- Evil corpus: `/app/corpus/evil/` (Contains intentional wait-for cycles)

Your Go detector must flag 100% of the evil corpus and 0% of the clean corpus.