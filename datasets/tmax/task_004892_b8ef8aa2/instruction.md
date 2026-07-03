You are an ETL data engineer building a new pipeline component in Go. We have a set of raw telemetry and purchase logs stored as JSON lines in `/home/user/raw_data.jsonl`. This data resembles a NoSQL document collection where the schema has evolved over time.

Your task is to write a Go program `/home/user/etl.go` that acts as a standalone NoSQL-style aggregation pipeline. It must read the JSON lines, reverse engineer the polymorphic data structures, perform aggregations, validate the output schema, and write a final JSON report.

Requirements for `/home/user/etl.go`:
1. It must take exactly one command-line argument: a target status string (e.g., `completed`). This acts as your parameterized filter.
2. It must read from `/home/user/raw_data.jsonl`.
3. It must filter the documents, keeping only those where the `status` matches the provided argument.
4. It must aggregate the total spend per `user_id`. 
   - Note: The schema of the documents is not strictly defined. Some documents have an `items` array (where each item has a `price` and `quantity`). Other newer documents just have a `total_amount` field. You must dynamically handle these variations (Data model reverse engineering).
5. Output Schema Validation: Before writing the output, your program must validate that every output record matches this strict schema:
   - `user_id`: string (cannot be empty)
   - `total_spend`: float64 (must be strictly greater than 0)
   If a user has a `total_spend` of 0 or less, they should be excluded from the final output.
6. The final output must be written to `/home/user/summary.json`. This file must contain a single JSON array of objects with the keys `"user_id"` and `"total_spend"`, ordered alphabetically by `user_id`.

Example execution:
`go run /home/user/etl.go completed`

Please write the complete Go code, ensure any necessary Go modules are initialized, and test it to verify that `/home/user/summary.json` is generated correctly.