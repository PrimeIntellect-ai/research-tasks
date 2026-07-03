You are acting as a Database Reliability Engineer. Recently, our backup systems were compromised by injection attacks embedded in graph database and SQL backup scripts. A senior engineer recorded a voice memo detailing the exact pattern of the malicious queries, but they have since left the company and we only have the audio file located at `/app/backup_memo.wav`. 

Your objectives are:
1. Extract the transcript from `/app/backup_memo.wav` (using tools like `whisper-cli` or similar transcription utilities you can install) to discover the specific malicious query patterns (which involve certain combinations of SPARQL/Cypher keywords, window function anomalies, and cross-representation mapping payloads).
2. Write a C program located at `/home/user/query_sanitizer.c` and compile it to `/home/user/query_sanitizer`.
3. The `query_sanitizer` must read query logs from standard input (one query per line) and output "SAFE" or "MALICIOUS" to standard output for each line.
4. Your sanitizer must correctly identify the malicious patterns described in the audio transcript, while allowing legitimate backup and pagination queries to pass through. 
5. The sanitizer must handle complex graph queries (SPARQL, Cypher) and SQL analytical aggregations (window functions).

When you have finished compiling your binary at `/home/user/query_sanitizer`, create a log file at `/home/user/done.txt` containing the word "READY". An automated verification suite will then run your binary against two hidden corpora: one containing exclusively safe backup queries, and one containing malicious injection queries. Your program must correctly classify 100% of both corpora.