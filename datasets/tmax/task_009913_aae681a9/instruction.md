You have recently joined a company and inherited a legacy Python codebase from a developer who abruptly left. Yesterday, the core backend service crashed catastrophically, and we need to figure out exactly what inputs caused the crash. 

You are provided with the following files left on the server:
1. `/home/user/app_mem.dump`: A raw memory dump of the crashed Python process.
2. `/home/user/logs/api_gateway.log`: Logs from the API gateway showing incoming requests.
3. `/home/user/logs/worker.log`: Logs from the specific worker process that crashed.
4. `/home/user/legacy_lib.py`: The library containing the main processing logic.

Your task is to perform a forensic analysis to reproduce the crash:

1. **Memory Analysis**: Extract the missing API secret key from `/home/user/app_mem.dump`. The key is stored in memory in the format `SECRET_KEY=<key_value>`.
2. **Timeline Reconstruction**: Correlate the timestamps and request IDs between `/home/user/logs/api_gateway.log` and `/home/user/logs/worker.log` to determine the exact `item_id` of the request that caused the worker to crash (the last request sent to the worker before it stopped logging).
3. **Reporting**: Create a JSON file at `/home/user/forensics_report.json` containing your findings. It must have exactly this format:
```json
{
  "secret_key": "<extracted_key>",
  "crash_item_id": "<identified_item_id>"
}
```
4. **Minimal Reproducible Example**: Create a Python script at `/home/user/reproduce.py` that imports the `process_data` function from `legacy_lib.py`. The script should call `process_data(secret_key, item_id)` using the exact strings you discovered to reliably trigger the crash. 

Do not modify `legacy_lib.py` or the log files.