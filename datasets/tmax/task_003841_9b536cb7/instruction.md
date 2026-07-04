You are a Database Reliability Engineer (DBRE) tasked with fixing our automated backup reconciliation system. A former engineer left a voice memo detailing a critical filtering rule for the reconciliation query before they left, but didn't implement it. 

Your task involves three steps:

1. **Information Extraction**:
There is an audio file at `/app/incident_report.wav`. You need to transcribe this audio file to understand the specific business logic and filtering rules required for the backup reconciliation query. You can use standard command-line tools or write a quick Python script using a library like `SpeechRecognition` or `whisper` to transcribe it.

2. **Schema Analysis**:
The system generates SQLite databases containing backup metadata. A sample database is located at `/app/sample_backup_meta.db`. 
Analyze the schema to understand the relationships between the `storage_nodes`, `backup_jobs`, and `job_chunks` tables.

3. **Reconciliation Script**:
Write a Python script at `/home/user/reconcile.py` that takes exactly one command-line argument: the path to a backup SQLite database file.
The script must connect to the provided SQLite database and execute a single comprehensive query (or a series of CTEs) that:
- Joins the relevant tables.
- Uses window functions to identify the *latest* successful backup job (based on `completed_at` timestamp) for *each* `storage_node`.
- Calculates the total size of all chunks associated with that latest successful job.
- Applies the specific exclusion rules mentioned in the audio recording.
- Outputs the result to `stdout` in strictly formatted CSV (without headers), sorted by `node_id` ascending. The columns should be: `node_id`, `node_name`, `latest_job_id`, `total_backup_bytes`.

Make sure your script only outputs the final CSV lines to `stdout` (no debugging print statements). The testing framework will run your script against thousands of randomly generated databases to ensure its output perfectly matches our reference implementation.