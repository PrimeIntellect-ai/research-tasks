As a data scientist, you are tasked with cleaning a legacy dataset and exposing it securely via a microservice.

We have a broken pipeline. A legacy system outputs a JSON-lines file at `/app/dirty_data.jsonl`, but it incorrectly double-escapes unicode sequences (e.g., it writes `\\u00E9` instead of `\u00E9`). 

Additionally, you have an auxiliary reference dataset at `/app/reference.csv`. 

Finally, there is an image artifact located at `/app/schema_rules.png`. This image contains a printed configuration snippet showing the required SQLite table name and a specific Authorization token for the API.

Your task is to write and run a Rust application that performs the following:
1. Extract the required `TABLE_NAME` and `AUTH_TOKEN` from `/app/schema_rules.png` (using OCR, `tesseract` is installed).
2. Read `/app/dirty_data.jsonl`.
3. Clean the data by fixing the double-escaped unicode sequences (convert `\\uXXXX` to the actual unicode characters) and parse the JSON.
4. Deduplicate the JSON-lines records based on the `user_id` field. If there are duplicates, keep the one with the highest `timestamp`.
5. Join the cleaned JSON data with `/app/reference.csv` on `user_id`.
6. Perform a bulk import of the joined, cleaned dataset into a new SQLite database located at `/home/user/cleaned.db`. The table must use the `TABLE_NAME` extracted from the image.
7. Start an HTTP server listening on `127.0.0.1:8080`. 
8. The server must expose a `GET /user/<user_id>` endpoint that queries the SQLite database and returns the joined record as a JSON object.
9. The server MUST reject any request to `/user/<user_id>` that does not include the header `Authorization: Bearer <AUTH_TOKEN>` (where `<AUTH_TOKEN>` is the exact token from the image) with a 401 Unauthorized status.

Use Rust for the data processing, SQLite import, and HTTP server. You may use standard bash commands for intermediate steps if necessary. Ensure the HTTP server remains running so it can be verified.