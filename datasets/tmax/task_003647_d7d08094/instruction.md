You are a log analyst investigating a series of connection drops across two different microservices. You have been provided with two log files that use entirely different formats and languages. 

Your task is to write a Python script at `/home/user/analyze_logs.py` that processes these logs, aligns their timestamps, filters for timeout errors, and outputs a consolidated report.

Here are the details of the input logs:
1. **Auth Service Logs** (`/home/user/logs/auth.log`):
   - Format: `[YYYY-MM-DDThh:mm:ssZ] LEVEL Message`
   - Language: English
   - Example: `[2023-10-25T14:30:15Z] INFO User logged in`

2. **Payment Service Logs** (`/home/user/logs/payment.log`):
   - Format: `EPOCH_MILLISECONDS [LEVEL] Message`
   - Language: Japanese (UTF-8)
   - Example: `1698244216500 [情報] セッション開始`

Your Python script must do the following:
1. Read both log files.
2. Filter for lines indicating a timeout. For the Auth service, look for the substring `timeout` (case-insensitive). For the Payment service, look for the substring `タイムアウト`.
3. Normalize all timestamps to standard ISO 8601 UTC format (`YYYY-MM-DDThh:mm:ss.sssZ`). Note: Auth logs don't have milliseconds, so pad them with `.000Z` (e.g., `2023-10-25T14:30:15.000Z`).
4. Consolidate the filtered logs into a single list and sort them strictly in chronological order (oldest to newest).
5. Output the sorted list to `/home/user/unified_timeouts.json` as a JSON array of objects. Each object must have exactly these keys:
   - `"timestamp"`: The normalized ISO 8601 string.
   - `"service"`: Either `"auth"` or `"payment"`.
   - `"message"`: The original message portion of the log (excluding the timestamp and level). For example, `Connection timeout` or `データベース タイムアウト`.
6. Implement pipeline logging: The script must append a log entry to `/home/user/pipeline.log` in exactly this format upon completion:
   `[SUCCESS] Processed logs: auth timeouts: <X>, payment timeouts: <Y>`
   (Where `<X>` and `<Y>` are the integer counts of timeout records found in each respective file).

Execute your script to produce the final JSON and pipeline log files.