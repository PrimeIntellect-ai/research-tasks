You are a Database Reliability Engineer (DBRE) tasked with auditing the backup storage costs for a specific database replication cluster. 

We have a legacy SQLite database containing historical backup logs, but the original schema documentation was lost. The only remaining documentation is an architectural diagram image located at `/app/schema_diagram.png`.

Your objectives:
1. **Reverse Engineer Data Model:** Analyze `/app/schema_diagram.png` (you can use `tesseract` or Python's `pytesseract`/`Pillow` to extract text from it) to understand the table names, relationships, and identify the "Master" node of the replication graph.
2. **Graph Traversal & Aggregation:** Write a Python script at `/home/user/summarize_chains.py` that connects to the SQLite database located at `/app/backup_metadata.db`. Your script must dynamically traverse the replication topology (starting from the Master node identified in the diagram) to find all downstream replicas (direct and indirect). Then, aggregate the total `bytes` backed up across this entire cluster (Master + all descendants) across all time.
3. **Index Optimization:** The `backup_metadata.db` database contains millions of records and is currently unoptimized. You must design and apply the correct index strategy directly to the SQLite database so your Python script runs as quickly as possible.
4. **Output Format:** Your script `/home/user/summarize_chains.py` should print *only* the final aggregated integer (the total backup size in bytes) to standard output.

We will evaluate your solution based on its execution time. To pass, your Python script must produce the exact correct integer and complete its execution in under 0.5 seconds.