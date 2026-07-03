You are a database reliability engineer managing backups for our organization's knowledge graph database. We have two critical tasks for you to complete to ensure the reliability and security of our backup metadata systems.

**Task 1: Analyze Backup Monitoring Video**
We have recorded a dashboard monitoring our backup pipeline in a video file located at `/app/backup_monitor.mp4`. 
Your task is to analyze this video and count the total number of frames where the exact word "FAIL" is clearly visible in the terminal output. 
Write the final integer count to `/home/user/failure_count.txt`. (You may use `ffmpeg` and OCR tools like `tesseract` which are available in the environment).

**Task 2: Build a Graph Query Sanitizer in C++**
Our backup metadata is queryable by downstream services using Cypher and SPARQL. We need a robust query filter to prevent malicious actions and enforce performance limits (e.g., pagination).

Write a C++ program at `/home/user/query_filter.cpp` and compile it to `/home/user/query_filter`. 
The executable must read a single query string from standard input (stdin) until EOF, and print exactly `ACCEPT` or `REJECT` (followed by a newline) to standard output.

Your filter must enforce the following rules:
1. **ACCEPT** standard, read-only queries that include a `LIMIT` clause (to enforce pagination/result filtering).
2. **REJECT** any query that attempts to modify data or schema (e.g., contains `DELETE`, `DROP`, `INSERT`, `CREATE`, `SET`, `REMOVE`).
3. **REJECT** any query that attempts to access restricted knowledge graph entities, specifically anything referencing `Credential`, `Secret`, or `Password`.
4. **REJECT** any query that lacks a `LIMIT` clause entirely.

Your implementation should be robust against variations in casing and whitespace. We will test your compiled `/home/user/query_filter` binary against an extensive, hidden suite of clean and adversarial queries to ensure it correctly classifies them.