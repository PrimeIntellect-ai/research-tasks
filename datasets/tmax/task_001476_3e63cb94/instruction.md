You are acting as a compliance officer auditing a voice-trading platform. You have been provided with an SQLite database `/app/trading.db` and an audio memo `/app/compliance_memo.wav` left by the Chief Compliance Officer. 

Your task is to build a simple HTTP API using Bash (you may use tools like `nc`, `socat`, or a lightweight Python server invoked from your Bash script) to serve the audit results.

Here are the requirements:
1. **Audio Transcription**: The file `/app/compliance_memo.wav` contains a dictated memo. You must transcribe it to identify the specific `user_id` targeted for this audit.
2. **Database Fix**: The `/app/trading.db` SQLite database has a table `trades` (id, user_id, amount, trade_date, status) and `users` (id, name). The index `idx_trades_user` is known to be corrupted and returns stale rows. You must bypass or fix this index to ensure accurate querying.
3. **Complex Querying**: Construct a SQL query that retrieves all trades for the targeted `user_id` where the `amount` is strictly greater than the rolling average of the user's previous 3 trades (ordered by `trade_date`).
4. **Service Setup**: Create an executable Bash script at `/home/user/serve_audit.sh` that starts an HTTP server listening on `127.0.0.1:8080`.
5. **Endpoints**:
   - `GET /target`: Returns a JSON object with the target user ID extracted from the audio. Schema: `{"target_user": <integer>}`.
   - `GET /report`: Returns a JSON array of the anomalous trades found by your query. Schema: `[{"trade_id": <integer>, "amount": <float>, "rolling_avg": <float>}, ...]`

Ensure your Bash script runs continuously in the foreground and correctly handles HTTP GET requests to these endpoints. You may use any command-line tools available in a standard Linux environment (like `sqlite3`, `jq`, `ffmpeg`, etc.) to achieve this.