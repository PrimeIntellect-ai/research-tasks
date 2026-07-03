You are an on-call engineer who just received a 3 AM page: the critical Payment Processor service has crashed, and worse, its configuration file was accidentally deleted by a rogue cleanup cron job just before the crash. 

You need to investigate the system state and extract the lost configuration data from a provided process memory dump, analyze the stack trace to find the point of failure, and reconstruct the timeline of events.

You are provided with the following files in `/home/user/`:
- `cron.log`: Logs from the system cron jobs.
- `payment.log`: Logs from the payment service.
- `crash.log`: The Python `faulthandler` stack trace generated when the service crashed.
- `memory_dump.bin`: A raw memory dump of the Python process taken right after the crash.

Your task is to determine:
1. The exact timestamp when the config file `/home/user/config.json` was deleted.
2. The exact timestamp when the payment service recorded the CRITICAL crash.
3. The exact line number in `/home/user/payment.py` where the segmentation fault occurred.
4. The secret API key that was stored in the deleted config file. It is still present in the process memory dump and is prefixed with `API_KEY_SECRET=`.

Write your findings to a JSON file at `/home/user/root_cause.json` with the following exact structure:
```json
{
  "api_key": "the_extracted_api_key_value",
  "deletion_time": "timestamp_of_deletion_from_logs",
  "crash_time": "timestamp_of_crash_from_logs",
  "crash_line": 123
}
```
Ensure the timestamps are extracted exactly as they appear in the logs (e.g., "YYYY-MM-DDThh:mm:ssZ"), and `crash_line` is an integer.