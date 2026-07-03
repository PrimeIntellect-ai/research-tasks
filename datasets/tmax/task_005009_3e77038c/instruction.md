You are tasked with building a streaming data processing pipeline for a configuration manager that tracks infrastructure changes. The configuration manager exports real-time event logs as a continuous JSON-lines (JSONL) stream.

We have a vendored pure-Bash JSON parser utility located at `/app/bash-json-parser/` that we use in environments where we cannot install `jq`. However, the configuration manager recently started emitting Unicode escape sequences (e.g., `\u0031`) in hostnames. The vendored parser has a known bug where it completely fails and drops lines containing any `\uXXXX` escape sequences.

Your task is to:
1. **Fix the Parser:** Identify and patch the deliberate bug in `/app/bash-json-parser/parse.sh` so that it successfully parses JSON lines containing standard Unicode escape sequences. 
2. **Build the Aggregator:** Create a Bash script at `/home/user/process_configs.sh` that reads the JSONL stream from standard input (`stdin`) and uses the fixed `/app/bash-json-parser/parse.sh` to extract the `value` field, but ONLY for events where the `metric` field is exactly `"memory_weight"`.
3. **Rolling Aggregation:** For the extracted `"memory_weight"` values, maintain a rolling sliding window of the last 5 values.
4. **Mathematical Output:** For every valid `"memory_weight"` event encountered, compute the current moving average of the window (using standard Bash integer division, i.e., floor division) and print it to standard output (`stdout`), one integer per line. Do not print anything else. If the window has fewer than 5 items, compute the average of the items currently in the window.

**Constraints:**
- You must write the solution using shell built-ins and standard POSIX utilities (like `awk`, `sed`, `grep`). Do not install or use `jq`, `python`, or `perl`.
- The script `/home/user/process_configs.sh` must be marked executable.
- The output must be bit-exact to the expected integer calculations, as an automated fuzzer will run your script against thousands of generated inputs to ensure correctness and stability.

Example input line:
`{"timestamp": 1700000000, "host": "srv-\u0031", "metric": "memory_weight", "value": 1024}`