You are a Database Reliability Engineer validating a hybrid-database backup. The backup validation jobs have just finished and generated metadata across our relational, document, and graph databases. 

You need to verify the consistency between our relational tables and their corresponding NoSQL document collections, using the mapping defined in our graph schema edges.

You are provided with three files in `/home/user/backup_metadata/`:
1. `relational_stats.txt`: A custom text output from the SQL backup tool. Each line contains table statistics in the format: `table: <table_name> | rows: <count>`
2. `document_stats.json`: A JSON file from the NoSQL backup tool containing an array of collection statistics.
3. `graph_schema.csv`: A CSV file defining the 1-to-1 relationships between the relational tables and document collections. The headers are `rel_table,doc_collection`.

Write a Python script to process these results. The script must cross-reference the counts of linked entities. A link is considered "consistent" if the `rows` count in the relational table exactly matches the `document_count` in the mapped NoSQL collection.

Your goal is to generate a JSON report at `/home/user/consistency_report.json`.
The output JSON must be a single dictionary where the keys are formatted as `<rel_table>_<doc_collection>` (based on the CSV mappings) and the values are boolean (`true` if consistent, `false` if inconsistent).

Example expected format for `/home/user/consistency_report.json`:
```json
{
  "customers_user_profiles": true,
  "transactions_receipts": false
}
```

Ensure your Python script correctly parses the files, performs the cross-representation mapping, and writes the final JSON file.