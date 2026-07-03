As a Database Reliability Engineer (DBRE), I need you to analyze our backup infrastructure's metadata to ensure data safety and identify misconfigurations. We use a SQLite database to track our backup chains and their storage locations.

The database is located at `/home/user/backup_metadata.db`. 
It has two tables:
1. `backups`: `id` (TEXT), `parent_id` (TEXT, can be NULL), `status` (TEXT - 'success', 'failed', 'running').
2. `storage`: `backup_id` (TEXT), `tier` (TEXT - 'hot', 'warm', 'cold').

A backup chain always starts with a full backup (where `parent_id` is NULL). Incremental backups link back to their parent via `parent_id`.

I need you to write a script in any language that performs the following:
1. **Recursive Hierarchy:** Use a recursive query or traversal to identify all backup chains.
2. **Knowledge Graph Pattern Matching:** We have a specific anti-pattern we need to catch. Identify all instances where a child backup is stored in a 'hot' storage tier, but its direct parent is stored in a 'cold' storage tier. This breaks our restoration SLA.
3. **Output Schema Validation:** Generate a report of these anomalies in JSON format at `/home/user/anomalies.json`. The JSON MUST strictly conform to the following JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "anomalies": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "child_backup_id": { "type": "string" },
          "parent_backup_id": { "type": "string" },
          "chain_root_id": { "type": "string", "description": "The ID of the full backup at the root of this chain" }
        },
        "required": ["child_backup_id", "parent_backup_id", "chain_root_id"]
      }
    }
  },
  "required": ["anomalies"]
}
```

The output file `/home/user/anomalies.json` must be correctly formatted and strictly adhere to this schema. If there are no anomalies, the `anomalies` array should be empty. Do not include backups with a 'failed' or 'running' status in your evaluation; only consider 'success' backups for the anomaly detection.