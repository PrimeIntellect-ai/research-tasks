You are a Database Reliability Engineer managing a complex backup dependency system. Recently, your backup metadata database crashed due to excessive load caused by poorly written queries.

Your tasks:
1. **Analyze the Incident Audio:**
   Listen to or transcribe the incident report located at `/app/incident_report.wav`. This audio file explains the exact root cause of the database crash, which was related to implicit cross joins (Cartesian products) in our graph queries.

2. **Develop a Query Filter (Python):**
   Based on the definitions provided in the audio, write a Python script at `/home/user/query_filter.py`.
   - The script must accept a single command-line argument: the path to a text file containing a single Cypher query.
   - It must analyze the query and determine if it is "clean" or "evil" (as defined in the audio).
   - If the query is "evil", the script MUST exit with status code `1`.
   - If the query is "clean", the script MUST exit with status code `0`.
   - The filter should be robust against variations in whitespace and capitalization.

3. **Graph Analytics (SQL):**
   We also need to identify the most critical backup jobs to prioritize their execution. The backup dependencies are temporarily exported to an SQLite database at `/app/backup_graph.db`.
   - Tables: `nodes(job_id TEXT)` and `edges(source_job TEXT, target_job TEXT)`.
   - Write a SQL query and save it to `/home/user/centrality.sql`.
   - The query must compute the degree centrality (total number of inbound and outbound edges) for each job.
   - Use a window function to compute the `rank` of each job based on its degree centrality (highest centrality = rank 1).
   - The output columns must be `job_id`, `centrality`, and `centrality_rank`.
   - Order the final results by `centrality_rank` ascending, then `job_id` ascending.

Make sure your Python script strictly adheres to the exit code requirements, as it will be tested against a hidden corpus of clean and evil queries.