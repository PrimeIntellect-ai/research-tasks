You are a Database Reliability Engineer (DBRE) responsible for the automated backup infrastructure. An automated emergency voicemail has just been deposited in your alert inbox at `/app/alert_019.wav`. 

Your task is to build a Python-based emergency backup retrieval API that operators can use to find the correct recovery files. 

Follow these steps:
1. **Process the Audio**: Transcribe `/app/alert_019.wav` to discover the affected `Tenant ID` and the emergency `Authorization Token`.
2. **Query the Backup Catalog**: A local SQLite database is located at `/app/backup_catalog.db`. It contains a table named `backups` with the following schema:
   - `id` (INTEGER PRIMARY KEY)
   - `tenant_id` (VARCHAR)
   - `datastore_type` (VARCHAR, e.g., 'postgres', 'mongo', 'redis')
   - `file_path` (VARCHAR)
   - `backup_timestamp` (DATETIME)
   - `size_bytes` (INTEGER)
3. **Build the Recovery API**: Create a Python HTTP web service (using Flask, FastAPI, or similar) listening on `0.0.0.0:8080`.
4. **Implement the Endpoint**: Expose a `GET /api/backups` endpoint that:
   - Requires an `Authorization: Bearer <TOKEN>` header. The token must exactly match the one spoken in the audio file. If missing or incorrect, return a `401 Unauthorized`.
   - Accepts `tenant_id` as a query parameter.
   - Accepts `page` (default 1) and `limit` (default 10) as query parameters for pagination.
   - Filters the SQLite catalog for the given `tenant_id`.
   - Sorts the results by `backup_timestamp` DESCENDING.
5. **Cross-Representation Schema Validation**: The API must map the relational SQL rows into the following strictly validated JSON NoSQL-style document schema:
   ```json
   {
     "request_metadata": {
       "tenant_id": "<string>",
       "page": <integer>,
       "limit": <integer>,
       "total_records": <integer>
     },
     "recovery_plan": {
       "postgres_backups": [
         {
           "path": "<file_path>",
           "timestamp": "<backup_timestamp>",
           "size_mb": <float, rounded to 2 decimal places, calculated from size_bytes>
         }
       ],
       "mongo_backups": [ ... ]
     }
   }
   ```
   Note: Map the relational records into lists grouped by `datastore_type` (only include datastore types that have records for that page).

Keep the API running in the foreground or background so it can be tested. Once the service is successfully running on port 8080, write a file at `/home/user/service_ready.txt` containing the word "READY" to signal that verification can begin.