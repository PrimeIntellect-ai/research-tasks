You are assisting a compliance officer in auditing a high-frequency trading system. We suspect that certain entities are artificially deadlocking concurrent transactions to manipulate market timings. 

An intercepted audio recording of a trader dictating the suspect transaction chains has been provided to you at `/app/audit_intercept.wav`. 

Your task is to build a C-based graph analytics service that processes this data and exposes an API for the compliance dashboard.

**Step 1: Transcription & Data Extraction**
1. Transcribe the audio file located at `/app/audit_intercept.wav`. (You may use tools like `whisper` or `ffmpeg` available in your environment).
2. The audio contains a dictated list of directed transactions in the format: "Transaction from account [X] to account [Y] with amount [Z]".
3. Parse this transcription into a structured CSV file at `/home/user/transactions.csv` with the schema: `source_account,target_account,amount`.

**Step 2: Graph Analytics Engine (in C)**
Write a C program that reads `/home/user/transactions.csv` and builds an in-memory directed graph. Implement the following analytics:
1. **Deadlock (Cycle) Detection:** Identify all accounts that are part of any directed cycle.
2. **Centrality:** Calculate the out-degree centrality for all accounts.
3. **Shortest Path:** Implement a mechanism to find the shortest path (fewest hops) between any two accounts.

**Step 3: Multi-Protocol Audit Service**
Your C program must start an HTTP server listening on `127.0.0.1:8080`. It must implement the following endpoints:
1. `GET /api/deadlocks`
   - Returns a JSON array of account IDs (integers) that are involved in a deadlock (cycle), sorted in ascending order.
2. `GET /api/centrality?limit=N`
   - Returns a JSON array of objects `[{"account": ID, "out_degree": score}]` for the top `N` accounts sorted by out-degree descending. If out-degrees are equal, sort by account ID ascending.
3. `GET /api/path?src=X&dst=Y`
   - Returns a JSON array representing the shortest path of account IDs from X to Y, e.g., `[X, A, B, Y]`. If no path exists, return `[]`.

**Requirements:**
- Your server must be written in C. You may use standard libraries or lightweight libraries like `libmicrohttpd` if you install them.
- Ensure the server runs continuously in the background or foreground once started.
- Create a log file at `/home/user/server.log` that logs every incoming request.