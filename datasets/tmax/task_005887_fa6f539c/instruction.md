You are an integration developer responsible for building a mock API server to test an upstream synchronization mechanism. You need to implement the server in Python, run it, and expose it for local integration testing.

Your task is to create a Python HTTP server in `/home/user/sync_server.py` using `Flask` or `FastAPI` (you may install them via pip). The server must run on port `8000`.

### API Specification
Implement a single endpoint:
**Endpoint:** `POST /api/v1/sync`
**Content-Type:** `application/json`

**Expected JSON Payload:**
```json
{
  "client_id": "string",
  "checksum": "string",
  "transactions": [
    {
      "id": "integer",
      "ts": "integer",
      "val": "string"
    }
  ]
}
```

### Business Logic & Requirements

1. **Checksum Validation:** 
   The `checksum` field must be the SHA256 hex digest of the concatenated string of all transaction `id`s exactly in the order they appear in the JSON array. 
   *(Example: if the payload contains transactions with IDs 105, then 102, the input to the hash function should be the string `"105102"`)*.
   If the checksum is invalid, return HTTP `400 Bad Request`.

2. **Rate Limiting:**
   A single `client_id` is allowed a maximum of **2 successful or unsuccessful requests per 10-second rolling window**. 
   If a client exceeds this limit, return HTTP `429 Too Many Requests`.

3. **Sorting, Merging, and State Updates:**
   If the request is valid and not rate-limited:
   - Read the local state file located at `/home/user/state/master.json`. This file contains a JSON array of existing transaction objects.
   - Merge the incoming transactions into the master list. **Ignore** any incoming transactions that have an `id` that already exists in the master list.
   - Sort the newly merged list of transactions ascending by `ts` (timestamp). If timestamps are tied, sort ascending by `id`.
   - Write the sorted list back to `/home/user/state/master.json`.

4. **Diff Logging:**
   For every successful synchronization (HTTP 200), append a single line to `/home/user/state/sync.log` documenting the new transactions added in this request.
   Format: `SYNC <client_id>: Added <count> transactions: <id_A>, <id_B>`
   The IDs in the log line must be listed in **ascending order** and comma-separated. If no new transactions were added, log `... Added 0 transactions: ` (with a trailing space).

### Execution Instructions
1. Implement the server in `/home/user/sync_server.py`.
2. Ensure the `/home/user/state` directory and `master.json` file exist. The initial `master.json` should contain: `[{"id": 100, "ts": 1690000000, "val": "INIT"}]`
3. Start the server in the background so it binds to `127.0.0.1:8000`.
4. Write the process ID (PID) of the server to `/home/user/server.pid` so our test suite can terminate it later.
5. Exit gracefully once the server is running in the background. Do not send any requests to the server yourself.