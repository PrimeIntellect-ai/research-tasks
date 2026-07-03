Our nightly data processing build is failing. The build script aggregates logs from two microservices, but it's currently crashing. You need to debug the pipeline and identify three root causes of the failures.

The build script is located at `/home/user/pipeline/build.py`. When you run it, it currently fails. 

Please investigate and find the following:
1. **Hidden Configuration File**: The script is trying to read a fallback configuration file when the primary one is missing, but it crashes because the fallback file is malformed. The path to this fallback file is not obvious in the code (it's loaded dynamically via a compiled binary dependency or obfuscated module). Use system call tracing on `build.py` to discover the exact absolute path of the configuration file it reads right before it crashes.
2. **Lost Decryption Key**: The script requires a `SECRET_KEY` environment variable to decrypt certain log entries. This key was accidentally committed to the git repository located at `/home/user/pipeline` in the past, but was subsequently removed. Search the git history to recover this string.
3. **Timeline Anomaly**: Once you provide the correct configuration and `SECRET_KEY` (by setting the `SECRET_KEY` env var and fixing or creating a valid config file to bypass the first crash), the script will crash again with a `ValueError` regarding timeline inconsistency. The script merges `/home/user/pipeline/logs/web.log` and `/home/user/pipeline/logs/db.log`. There is exactly one `transaction_id` where the `DB_COMMIT` event occurs *chronologically before* the `WEB_REQUEST` event. Find this `transaction_id`.

Once you have identified all three pieces of information, create a JSON file at `/home/user/debug_report.json` with the following exact structure:
```json
{
  "hidden_config_path": "<absolute_path_to_the_file_discovered_via_tracing>",
  "recovered_key": "<the_secret_key_from_git_history>",
  "failing_transaction_id": "<the_transaction_id_with_the_timeline_anomaly>"
}
```