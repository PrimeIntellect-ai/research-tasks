You are an AI assistant helping a compliance officer perform a technical audit of internal financial flows. We suspect a money laundering ring, and a whistleblower has left us an anonymous voicemail indicating the starting node of the suspicious transaction graph.

You must perform the following steps in a Linux terminal:

1. **Extract the Target:** You have been provided an audio recording of the whistleblower at `/app/whistleblower.wav`. Transcribe this audio to identify the "source account ID" mentioned in the recording.
2. **Graph Processing & Optimization:** You have access to a SQLite database at `/app/finance.db`. It contains a single table representing a directed graph of money flows: `transfers(tx_id TEXT, from_acct TEXT, to_acct TEXT, amount REAL, tx_date TEXT)`.
   - Analyze the schema and write an optimized recursive query to find *all* accounts that received funds directly or indirectly originating from the source account. 
   - You must design and apply an index strategy (e.g., via `sqlite3`) to optimize the execution plan of your recursive traversal. 
3. **Expose the Audit Results:** The compliance auditing software expects to retrieve this list programmatically. 
   - Bring up an HTTP service listening exactly on `0.0.0.0:9000`.
   - The service must respond to `GET /chain` requests.
   - It must require the HTTP header `X-Compliance-Auth: auditor_key`. (Return 403 Forbidden otherwise).
   - If authorized, it must return an `application/json` response containing a flat JSON array of the downstream account IDs (strings), deduplicated and sorted in ascending order. (e.g., `["1001", "1002", "1005"]`).

Ensure your service remains running so the automated verifier can query it. You can use standard tools available in a Linux environment (e.g., Python, Bash, sqlite3, socat, ffmpeg, whisper).