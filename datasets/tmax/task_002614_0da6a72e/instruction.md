You are a data engineer building an ETL pipeline that combines relational data and out-of-band audio instructions to feed into a graph analytics engine. 

You have been provided with two artifacts:
1. An SQLite database at `/app/company.db`.
2. An audio voicemail file at `/app/overrides.wav`.

**Step 1: Extract Active Users**
The `/app/company.db` database contains an `employees` table (columns: `emp_id`, `name`, `status`) and an `employee_edges` table (columns: `source_id`, `target_id`). 
Recently, the `idx_status` index on the `employees` table became corrupted, causing it to return stale rows. If you do a standard `SELECT` with a `WHERE status = 'active'` clause, the query optimizer uses this corrupted index and returns incorrect records.
Analyze the query plan and extract the *true* list of active employees by forcing SQLite to bypass the corrupted index (e.g., forcing a full table scan or dropping the index). 

**Step 2: Transcribe and Aggregate Edge Data**
The `/app/overrides.wav` file contains a spoken message from the HR director detailing recent reporting changes. You must transcribe this audio to extract additional directed edges. The audio will explicitly state rules like "add an edge from employee X to employee Y".
Combine the directed edges found in the `employee_edges` table (filtering so that both `source_id` and `target_id` are *true* active employees) with the new edges extracted from the audio (which should also be added to your graph, provided the nodes are active employees).

**Step 3: Graph Analytics Server**
Using the final combined data, build a directed graph. You must calculate the PageRank centrality for all nodes in this graph (use a standard PageRank algorithm with a damping factor of 0.85).

Finally, write and start an HTTP server (e.g., in Python using Flask/FastAPI or Ruby/Node.js) that listens on `127.0.0.1:8000`. 
Your service must expose the following endpoint:
* `GET /api/centrality?node=<emp_id>`
* It must return a JSON response in the exact format: `{"node": <emp_id>, "centrality": <float>}`.

Leave the server running in the background. Do not implement authentication. The automated verifier will test your server's responses using HTTP GET requests.