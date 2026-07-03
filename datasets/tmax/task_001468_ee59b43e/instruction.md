You are a data engineer debugging a broken multi-stage ETL pipeline. The lead architect left you a voice memo detailing the exact issues, which involve a SQL performance bug, a NoSQL injection vulnerability, and a broken graph traversal script. 

Your goals are to transcribe the architect's memo and implement the three requested fixes.

**Step 1: Audio Transcription & Requirements Gathering**
An audio file has been placed at `/app/audio/architect_memo.wav`. You must transcribe this audio (using tools like `whisper` or `ffmpeg` available in your environment) to understand the architectural rules and business logic for the next steps.

**Step 2: NoSQL Aggregation Sanitizer**
We are receiving NoSQL query payloads from an upstream service, but some are poorly optimized or outright malicious, causing the database to hang. 
Based on the exact criteria mentioned in the audio file, write a Python CLI tool at `/home/user/sanitizer.py`.
- **Usage:** `python /home/user/sanitizer.py <path_to_pipeline.json>`
- **Behavior:** The script must parse the MongoDB aggregation pipeline (provided as a JSON array in the file). If the query violates the rules specified in the audio (related to index strategies and banned operators), it must print "REJECT" and exit with status code `1`. If the query is compliant, it must print "ACCEPT" and exit with status code `0`.
- **Validation:** We have provided an adversarial corpus. You must ensure your sanitizer strictly accepts all files in `/app/corpus/clean/` and strictly rejects all files in `/app/corpus/evil/`.

**Step 3: Fix Implicit Cross Join & Add Window Function**
Our relational ETL step is timing out. A downstream query (`/app/etl/bad_query.sql`) was written incorrectly, resulting in an implicit cross join that explodes the row count. 
- Reverse engineer the tables using the DDL in `/app/etl/schema.sql`.
- Create a new file `/home/user/fix_query.sql`. 
- Fix the join logic so it correctly links the tables. 
- Furthermore, as requested in the audio, apply a window function to filter the results so that only the specified "latest" or "top" records per entity are returned.

**Step 4: Referral Graph Traversal**
The ETL pipeline processes a user referral network, stored as an adjacency list in `/app/etl/referrals.json`. 
- Write a Python script at `/home/user/graph_path.py`.
- **Usage:** `python /home/user/graph_path.py <source_node> <target_node>`
- **Behavior:** It must compute and print the shortest path (as a comma-separated list of node IDs) between the source and target using standard graph traversal logic. If no path exists, print "NONE".

Ensure all output files are placed exactly at the `/home/user/` paths requested.