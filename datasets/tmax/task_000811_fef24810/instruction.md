You are a data analyst investigating transaction concurrency issues. We are analyzing CSV files that represent "wait-for" graphs between concurrent transactions. Each row in a CSV file contains `waiting_txn_id,holding_txn_id`, indicating that a transaction is blocked waiting for a lock held by another transaction.

Your objective is to write a Bash script that acts as a deadlock detector and schema validator. 

First, examine the video file located at `/app/transaction_visualization.mp4`. This video is a screen recording of a dashboard. Frame extraction and OCR (e.g., using `ffmpeg` and `tesseract`) will reveal a frame containing a specific regex pattern labeled "STRICT CSV SCHEMA:". You must extract this regex pattern.

Next, create a Bash script at `/home/user/detect_deadlocks.sh`. The script must take a single file path as an argument (a CSV file) and perform the following:
1. **Output Schema Validation:** Validate every line of the input CSV against the regex pattern extracted from the video. If any line fails to match the pattern, the script must immediately print exactly `INVALID_SCHEMA` to stdout and exit with code 1.
2. **Recursive Graph Traversal:** If the schema is valid, parse the dependencies and traverse the graph to identify if there are any cycles (deadlocks). A deadlock occurs if a transaction is waiting on a lock that is held by another transaction which, through a chain of dependencies, is waiting on the first transaction (e.g., A waits for B, B waits for C, C waits for A).
3. **Classification:** 
   - If a cycle (deadlock) is found, print exactly `DEADLOCK` to stdout and exit with code 0.
   - If the graph is a Directed Acyclic Graph (DAG) with no cycles, print exactly `VALID` to stdout and exit with code 0.

Constraints:
- You must write the solution strictly using Bash, shell built-ins, coreutils (like `awk`, `grep`, `sed`), and standard CLI tools.
- Do not use Python, Perl, or Ruby for the deadlock detection script.

You must ensure your script correctly classifies files without throwing false positives or missing deep, multi-level recursive deadlocks.