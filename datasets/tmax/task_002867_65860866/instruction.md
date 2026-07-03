You are a log analyst investigating patterns in an application's event stream. The application logs are in JSON-Lines format. However, due to a known bug, the `message` field in these logs frequently contains corrupted and invalid unicode escape sequences (e.g., `\u00X9`, `\uZZZZ`) which cause standard JSON parsers like `jq` or `python -m json.tool` to break and fail entirely.

You have been provided with an image file at `/app/baseline_target.png` which contains a single reference baseline value printed as text.

Your task is to write a robust Bash script at `/home/user/analyze.sh` that processes these JSON-lines from standard input, calculates summary statistics, and outputs a specific distance metric. 

Here are the precise requirements for `/home/user/analyze.sh`:
1. **Read from STDIN**: The script must read JSON-lines from standard input.
2. **Robust Extraction**: Bypass the unicode parsing errors to extract the numeric `value` field from each JSON object. The lines will be structured similar to: `{"timestamp": 1700000000, "value": 45.2, "message": "error \uZZZZ"}`.
3. **Interpolation/Imputation**: The `value` field is sometimes `null` or missing. You must impute missing values using forward-fill (carry forward the last seen valid numeric value). If the very first line's value is missing or `null`, use `0` as the initial valid value.
4. **Summary Statistics**: Compute the arithmetic mean of all the values (after imputation) across the entire input stream.
5. **Distance Computation**: Read the reference baseline value from the `/app/baseline_target.png` image (using a tool like `tesseract`). Calculate the absolute difference between your computed mean and this reference baseline.
6. **Output**: Print ONLY the final absolute distance to standard output, formatted to exactly two decimal places (e.g., `12.34`). Do not print any other debugging information or text.

Your script must be written purely in Bash (relying on shell built-ins, standard coreutils, `sed`, `awk`, `grep`, `bc`, etc.). Do not write a Python or Node.js script.

Ensure your script is executable (`chmod +x /home/user/analyze.sh`) and functions non-interactively as it will later be scheduled via `cron` to run on streaming log pipelines.