You are an MLOps engineer maintaining an ETL pipeline that processes experiment artifact metadata. Recently, some artifact logs have been injected with malicious payloads targeting our deployment scripts.

You have been given a screenshot of our current experiment specifications located at `/app/specs.png`. 

Your task is to:
1. Extract the target metric name from the image `/app/specs.png` (using OCR tools like `tesseract`).
2. Write a Bash script at `/home/user/filter_artifacts.sh` that takes a single argument: the path to a JSON log file.
3. The script must validate the JSON file and exit with code `0` if it is completely safe and valid, or exit with code `1` if it is invalid or malicious.

A JSON log file is considered **invalid/malicious** if ANY of the following are true:
- The `metric` field in the JSON does not exactly match the target metric name found in `/app/specs.png`.
- The `model_path` field contains any shell metacharacters that could lead to command injection (specifically `;`, `|`, `&`, `$`, `` ` ``) or path traversal attempts (specifically the substring `..`).

A JSON log file is considered **valid** (clean) if it is well-formed, matches the exact target metric, and has a safe `model_path` (containing only alphanumeric characters, dashes, underscores, and single forward slashes `/`, with no traversal sequences).

Ensure your script is executable (`chmod +x /home/user/filter_artifacts.sh`). You must use Bash as the primary language, but you can use common tools like `jq`, `grep`, and `awk`.