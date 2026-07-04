You are a log analyst investigating anomalous metric injections in our system. We have discovered that an attacker has been injecting fake log entries. We managed to recover the compiled tool the attacker used to generate the malicious metric values, which is located at `/app/fake_metric_gen`. 

This tool is a stripped binary. We know it takes two integer arguments: a Unix timestamp (in seconds) and a `user_id`. It outputs a calculated `metric_value` that the attacker then injects into our CSV logs.

Your task is to create a Python script at `/home/user/filter_logs.py` that acts as a sanitizer for our log files. 

Requirements for `/home/user/filter_logs.py`:
1. It must accept a single command-line argument: the path to a CSV log file.
2. It must read the CSV file. The CSV contains a header and three columns: `timestamp_iso` (ISO 8601 string, UTC), `user_id` (integer), and `metric_value` (integer).
3. It must convert the `timestamp_iso` to a Unix timestamp (integer seconds).
4. It must mathematically determine if the `metric_value` in the log matches the output that the attacker's tool (`/app/fake_metric_gen`) would produce for that timestamp and `user_id`.
5. It must drop (filter out) any row that matches the attacker's generated value.
6. It must print the remaining "clean" rows to standard output (`stdout`) in the exact same CSV format (including the header).

You will need to interact with `/app/fake_metric_gen` to figure out the mathematical relationship it uses, and then implement that logic efficiently in your Python script so it can process large files without invoking the binary for every single row.

Your solution will be tested against hidden corpora of purely malicious logs and purely clean logs to ensure it perfectly separates them.