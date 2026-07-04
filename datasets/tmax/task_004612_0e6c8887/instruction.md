You are acting as a technical compliance officer auditing an organization's internal transaction network. 

We have intercepted an automated compliance alert audio file located at `/app/compliance_alert.wav`. You need to process this audio to extract two critical pieces of information:
1. The **target entity** name.
2. The **traversal depth** (an integer).

Additionally, you have been provided an undocumented SQLite database at `/home/user/audit_records.db`. This database contains a graph-like structure representing financial transactions and corporate relationships.

Your tasks are:
1. **Audio Analysis:** Transcribe `/app/compliance_alert.wav` to discover the target entity and the traversal depth.
2. **Schema Reverse Engineering:** Analyze `/home/user/audit_records.db`. Identify how entities (nodes) and their relationships (edges) are stored. 
3. **Graph Processing:** Formulate an optimized query (e.g., using a Recursive CTE) to traverse the relationships from any given entity up to the exact traversal depth specified in the audio.
4. **Service Integration:** Create and start an HTTP web service listening on `127.0.0.1:8080`. The service must implement the following endpoints:
   - `GET /api/alert_info`: Returns a JSON object with the keys `target` (string) and `depth` (integer) extracted from the audio.
   - `GET /api/trace?entity=NAME`: Returns a JSON array of strings containing the names of all entities within the specified traversal depth from the given `entity` (inclusive of the queried entity itself). The array must be sorted alphabetically and contain no duplicates.

Do not use authentication. Ensure the service remains running in the foreground or background so that our automated verification tools can issue HTTP requests against it. You may use any combination of languages (e.g., Python, Node.js, Shell, SQL) to accomplish this.