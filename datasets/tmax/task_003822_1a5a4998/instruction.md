You are an observability engineer tuning the log ingestion pipeline for your team's dashboards. Recently, a series of malformed metric logs have been crashing the dashboard backend.

You need to implement a lightweight log sanitiser in Go that filters out these malicious or malformed entries before they reach the dashboard.

We have provided a scaffolding project in `/home/user/log-sanitiser/`. It uses a vendored third-party JSON parsing library located at `/app/vendor/github.com/buger/jsonparser`. 

However, there are two problems you must solve:
1. **Broken Dependency:** The vendored `jsonparser` package is failing to build on our Linux environment. The previous engineer made a mistake in its configuration. You must find and fix the perturbation in the vendored package (hint: check its build configuration or Makefile) so it compiles successfully on Linux `amd64`.
2. **Implement the Sanitiser:** Complete the `main.go` file in `/home/user/log-sanitiser/`. 
   - The program should accept a single command-line argument: the path to a log file.
   - The log file contains one JSON object per line.
   - Your program must read the file line by line and print ONLY the "clean" logs to standard output (one per line).
   - A log line is considered "evil" (and must be completely ignored/dropped) if ANY of the following are true:
     - The `metric_value` field is missing.
     - The `metric_value` field is a JSON string instead of a JSON number.
     - The `metric_name` field contains the exact substring `DROP_ME`.
   - Your program must exit with status code 0 if it successfully processes the file.

To test your implementation, we have provided two directories containing sample log files:
- `/home/user/corpus/clean/` : Contains logs that are 100% valid. Your program must output these exactly as they are.
- `/home/user/corpus/evil/` : Contains logs that are designed to break the dashboard. Your program must output absolutely nothing for these lines.

Ensure your Go code is fully self-contained in `/home/user/log-sanitiser/main.go` and uses the vendored library to parse the JSON. Do not use external libraries other than the standard library and the provided vendored package.