Hello, I am a researcher trying to organize a dataset of academic citations, but I'm running into some serious data integrity issues.

I have an SQLite database located at `/home/user/research_data.db`. It contains a citation graph, but a synchronization bug caused duplicate "stale" rows to be inserted. 

Here is the schema:
- `papers` (id TEXT, title TEXT, metadata_json TEXT)
- `citations` (source_id TEXT, target_id TEXT)

The `metadata_json` column contains NoSQL-style JSON data, including an `"updated_at"` timestamp (integer) and a `"categories"` array (list of strings).

Because of the bug, the `papers` table contains multiple rows with the *same* `id`. Only the row with the maximum `"updated_at"` value in `metadata_json` is the valid, active record. The `citations` table also contains exact duplicates.

Your task is to:
1. Write a Python script that connects to this database and constructs a cleaned, directed citation graph. A citation from paper A to paper B is only valid if both A and B exist as valid papers (using the latest `updated_at` rule) AND the citation edge itself is considered after deduplicating the `citations` table.
2. Find the shortest directed path from the paper with ID `"P-START"` to the paper with ID `"P-END"`.
3. Extract all the `"categories"` from the `metadata_json` of every paper along this shortest path (inclusive of start and end).
4. Save the results to `/home/user/path_results.json` in the exact following JSON format:

```json
{
  "path": ["P-START", "P-NEXT", ..., "P-END"],
  "categories": ["CategoryA", "CategoryB", "CategoryC"]
}
```
*Note: The `categories` array should contain all unique categories found along the path, sorted alphabetically.*

If there are multiple shortest paths, choose the one where the sequence of paper IDs is lexicographically smallest.

Please write the Python script, execute it, and ensure the output file is generated correctly.