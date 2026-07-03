You are an AI assistant helping a bioinformatics researcher organize a fragmented dataset into a unified graph representation.

The researcher has experimental data stored in an SQLite database and subject metadata stored in a JSON Lines format. Due to a previous pipeline failure, the caching table in the database contains stale and corrupted rows.

Here are the details of the available data:
1. **Relational Data**: `/home/user/research_data.db` (SQLite)
   - Table `subjects`: `id` (INTEGER), `name` (TEXT)
   - Table `measurements`: `id` (INTEGER), `subject_id` (INTEGER), `timestamp` (DATETIME), `value` (REAL)
   - Table `latest_measurements_cache`: `subject_id` (INTEGER), `latest_timestamp` (DATETIME), `value` (REAL)
   *WARNING:* The `latest_measurements_cache` table is known to be corrupted and contains stale rows. You MUST bypass it entirely. Instead, deduce the true latest measurement for each subject by analyzing the append-only `measurements` table and grouping by `subject_id` to find the row with the maximum `timestamp`.

2. **Document Data**: `/home/user/metadata.jsonl` (JSON Lines)
   - Each line is a JSON object with keys: `subject_id` (int), `attributes` (dict), and `related_subjects` (list of ints representing directed edges from this subject to others).

Your task is to write a Python script (or use bash utilities) to cross-reference the relational database and the document metadata, and output a unified graph representation. 

The output MUST be written to `/home/user/unified_graph.json` and must strictly adhere to the following JSON schema representation:
```json
{
  "nodes": [
    {
      "id": <subject_id>,
      "name": "<subject_name>",
      "latest_value": <true_latest_measurement_value_or_null_if_none>,
      "attributes": { ... }
    }
  ],
  "edges": [
    {
      "source": <subject_id>,
      "target": <related_subject_id>
    }
  ]
}
```

Constraints and Instructions:
- "nodes" must be a list of objects, sorted in ascending order by "id".
- "edges" must be a list of objects, sorted first by "source" ascending, then by "target" ascending.
- Ensure only edges where both the source and target exist in the `subjects` table are included (drop dangling edges).
- Do not modify the original `.db` or `.jsonl` files.
- The final output file `/home/user/unified_graph.json` must be standard, strictly formatted JSON.