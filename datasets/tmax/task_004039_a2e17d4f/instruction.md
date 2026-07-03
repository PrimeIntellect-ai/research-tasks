You are a Site Reliability Engineer (SRE) monitoring the uptime of an internal mathematics service. The service is written in Rust and aggregates numerical data from sensors. The service reads a batch of sensor data from a JSON file, decodes a Base64-encoded string for each sensor, and calculates the mathematical sum of the comma-separated integers within.

Recently, the service has been experiencing intermittent crashes in production, affecting our uptime metrics. The application panics when it encounters corrupted or malformed payloads.

We have captured the state of the system in the `/home/user/` directory:
- `/home/user/metric_service/`: The Cargo project containing the Rust service.
- `/home/user/data.json`: A production data sample that consistently reproduces the crash.
- `/home/user/crash.log`: The panic stack trace captured from the last crash.

**Your Task:**
1. Analyze the stack trace and the source code in `/home/user/metric_service/` to determine the root cause of the panics.
2. Fix the Rust code so that it handles corrupted input gracefully. Specifically, if a record fails Base64 decoding, UTF-8 conversion, or integer parsing, the program must catch the error and print `<id>:ERROR` to stdout instead of panicking.
3. For valid records, the program must continue to print `<id>:<sum>` to stdout (e.g., `s1:60`).
4. Build and run your fixed program against `/home/user/data.json`.
5. Redirect the successful standard output of your fixed program to `/home/user/output.txt`.

Ensure your output matches the exact format described, with one record per line in the order they appear in the JSON file. Do not change the JSON file.