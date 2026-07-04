You are an operations engineer triaging a recent application crash in a production environment. A Python worker crashed while calculating risk scores, leaving behind an application log and a raw memory dump of the worker process.

You have access to the following files in `/home/user/incident/`:
1. `app.log` - Contains the application logs and the Python traceback of the crash.
2. `crash.dmp` - A raw memory dump of the worker process at the time of the crash.

Your task is to perform forensics on these files to identify the root cause of the incident. 
1. Analyze `app.log` to identify the exact Python Exception type that caused the crash.
2. Extract strings from the `crash.dmp` file to find the context of the last processed record. Look for a string starting with `CURRENT_RECORD_CTX:`.
3. Identify the `user_id` from that context string.

Finally, create a JSON report at `/home/user/incident/report.json` with exactly the following format:
```json
{
  "user_id": "<extracted_user_id>",
  "exception": "<extracted_exception_type>"
}
```
Replace `<extracted_user_id>` and `<extracted_exception_type>` with the actual values you found. Do not include any other keys or formatting in the JSON file.