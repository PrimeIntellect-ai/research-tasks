You are a Database Reliability Engineer investigating a complex issue with our distributed backup system. Recently, a script error caused some implicit cross joins in our metadata, creating ghost backup dependencies. We have a video recording of the backup monitor's terminal output during the incident at `/app/backup_monitor_incident.mp4`. 

Your task is to build a C++ HTTP service that serves the corrected backup dependency graph and associated analytics.

1. **Video Analysis**: Use `ffmpeg` and OCR tools (like `tesseract`, which you may need to install) to extract the text from the video at `/app/backup_monitor_incident.mp4`. The video shows terminal logs where each frame might contain a backup job entry in the format: `Job: <JobID> | DependsOn: <ParentJobID> | Size: <Bytes>`. 
2. **Data Processing & Graph Construction**: Parse the extracted text. Reconstruct the NoSQL-style document collection of backup jobs. Clean up the data by removing duplicate dependencies (the "ghost" cross joins). Build a dependency graph of the backup jobs.
3. **Graph Analytics**: Compute the in-degree (number of dependents) for each backup job. Identify the top 3 most critical backups (highest in-degree).
4. **C++ HTTP Service**: Write a C++ HTTP server (you can use `httplib` or `Boost.Beast`, but keep it self-contained or install the necessary libraries). 
   - The server must listen on `127.0.0.1:8080`.
   - Endpoint `/api/backups`: Returns a JSON array of all backup jobs, validating the output schema matches: `{"id": string, "depends_on": [string], "size": number, "criticality_score": number}`.
   - Endpoint `/api/critical`: Returns a JSON array of the top 3 critical backup IDs.
   - Endpoint `/api/summary`: Returns a cross-query aggregation summarizing the total size of all backups and the total number of unique dependencies.

Make sure your C++ server is running in the background and listening on port 8080 when you complete your interactions. Output your compilation command and start the server. Do not shut the server down.