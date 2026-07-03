You are a Database Reliability Engineer investigating why the automated nightly database backups are failing. The legacy database system does not have a modern logging system but instead outputs its transaction and locking state to a dedicated video monitor. We have captured a recording of this monitor during the backup failure window, located at `/app/db_monitor.mp4`.

Your task is to analyze this video, extract the transaction wait-for graph, detect deadlocks using recursive graph querying, and expose your findings via a local HTTP API for our automated remediation system.

**Step 1: Video Analysis**
Extract the frames from `/app/db_monitor.mp4`. The video displays a sequence of database lock events in black monospace text on a white background. 
Events appear as new lines over time in the following formats:
- `Tx[ID] ACQUIRE [Resource]` (Transaction successfully locked a resource)
- `Tx[ID] WAIT [Resource]` (Transaction is blocked waiting for a resource)

Use `ffmpeg` and `tesseract` (OCR) to read these events. Collate all unique events that appear in the video.

**Step 2: Graph Construction and Querying**
Using Bash and `sqlite3`, construct a Wait-For Graph. A transaction $T_1$ waits for $T_2$ if $T_1$ is waiting for a resource that $T_2$ has acquired.
1. Create an SQLite database at `/home/user/locks.db`.
2. Write a recursive Common Table Expression (CTE) in SQL to traverse the wait-for graph and identify any cycle of transactions (a deadlock).
3. Compute the "blocker centrality" (the in-degree in the wait-for graph) to find which transaction holds resources that the highest number of *other* transactions are waiting for.

**Step 3: Remediation API**
Create a service that listens on `127.0.0.1:9090` using HTTP. You must use Bash (e.g., using `socat`, `nc`, or a simple Python wrapper invoked from bash) to serve the following endpoints:

- `GET /api/deadlock`
  Must return a `200 OK` with a plain text, comma-separated list of the Transaction IDs involved in the deadlock cycle, sorted alphabetically (e.g., `TxA,TxB,TxC`).

- `GET /api/blocker`
  Must return a `200 OK` with a plain text response containing exactly the Transaction ID with the highest blocker centrality (e.g., `TxD`). If there is a tie, return the one that comes first alphabetically.

Keep the service running in the foreground or background so it can be queried by our verification systems.