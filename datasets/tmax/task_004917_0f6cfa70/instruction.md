You are a log analyst investigating a series of suspicious login attempts across multiple microservices. You have been provided with three log files in different formats, representing the Authentication service, the Database service, and the API Gateway.

Your task is to write a Python script at `/home/user/analyze_logs.py` that correlates these logs, applies validation checks, and generates a structured incident report.

### Log Files
All logs are located in `/home/user/logs/` and are recorded in UTC.
1. **`auth.jsonl`** (JSON Lines format):
   Contains authentication events.
   Format: `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "event": "<event_type>", "ip": "<ip_address>", "user": "<username>"}`

2. **`api.csv`** (CSV format):
   Contains API requests.
   Columns: `timestamp,ip,endpoint,status`
   Timestamp format: `YYYY-MM-DDTHH:MM:SSZ`

3. **`db.log`** (Plain text):
   Contains database operations and errors.
   Format: `[DD/MMM/YYYY:HH:MM:SS +0000] <LEVEL>: <Message>`

### Requirements

**Phase 1: Validation Checkpoint**
Before performing any analysis, your script must validate that the entries within *each* log file are strictly in chronological order (timestamps are non-decreasing). 
- If any file is out of chronological order, your script must immediately write exactly `ERROR: INVALID_ORDER <filename>` (e.g., `ERROR: INVALID_ORDER db.log`) to `/home/user/error.log` and exit with code 1.
- If all files are valid, proceed to Phase 2.

**Phase 2: Data Correlation**
Find all instances of `login_failed` events in `auth.jsonl`. For each failed login:
1. Identify all API requests in `api.csv` originating from the *same IP address* that occurred within a **10-second window** (i.e., exactly -5 seconds to +5 seconds, inclusive) of the failed login timestamp. Count these requests.
2. Identify all DB log entries in `db.log` whose `<Message>` contains the exact string `user <username>` (where `<username>` is the user from the failed login) AND occurred within the same **10-second window** (-5 to +5 seconds, inclusive) of the failed login timestamp. Extract the `<LEVEL>: <Message>` part of these matched logs.

**Phase 3: Template-Based Report Generation**
Generate a Markdown report at `/home/user/report.md` using the exact structure below. Sort the incidents in chronological order based on the `auth_timestamp`.

```markdown
# Incident Report

## Failed Login for user: {username} at {auth_timestamp}
- IP Address: {ip_address}
- Matched API Requests: {count_of_matched_api_requests}
- DB Logs:
  - {db_log_level_and_message_1}
  - {db_log_level_and_message_2}
```
*Note: If there are no DB logs matched for a failed login, the `DB Logs:` section should output `- None` instead of the list.*
*Separate each incident section with a single blank line.*

Run your script to produce `/home/user/report.md` (or `/home/user/error.log` if validation fails).