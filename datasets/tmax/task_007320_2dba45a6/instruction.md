You have recently inherited an unfamiliar legacy codebase located in `/home/user/legacy_repo`. When you try to run the main data pipeline, it crashes immediately. 

The previous developer left behind a few artifacts:
1. A crash log located at `/home/user/legacy_repo/logs/crash.log`.
2. A Git repository containing the codebase history.
3. A packet capture of a successful execution from last year, located at `/home/user/legacy_repo/pcap/session.pcap`.

Your task is to debug the cause of the failure by analyzing these artifacts. Specifically:
1. Examine the traceback in the crash log to understand what the application is trying to do and why it fails.
2. The application requires an API key that is currently missing from the configuration. This key was accidentally committed to the Git repository in the past, but was subsequently removed. Recover this API key using Git history forensics.
3. The application is trying to send data to an endpoint, but the endpoint URL in the current code is corrupted/missing. Extract the correct HTTP POST request path (endpoint) from the provided packet capture (`session.pcap`).
4. You may write any scripts (Python, bash, etc.) necessary to extract the data from the pcap or Git repository.

Once you have recovered the required information, output your findings to a JSON file at `/home/user/fix_info.json` with exactly the following structure:
```json
{
  "api_key": "<recovered_api_key>",
  "endpoint": "<recovered_endpoint_path>"
}
```
For example, if the key is `abc-123` and the endpoint is `/api/v1/submit`, the values should reflect that precisely.