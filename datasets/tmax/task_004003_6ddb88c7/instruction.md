You are an observability engineer tasked with feeding Git deployment events into a custom dashboard. To do this, you need to configure a Git `post-receive` hook written in Rust that logs push events in a highly specific JSON format.

A bare Git repository already exists at `/home/user/metrics-dashboard.git`.

Your task:
1. Write a Rust program and compile it. Place the compiled executable at exactly `/home/user/metrics-dashboard.git/hooks/post-receive`. Ensure it has executable permissions (`755`).
2. The `post-receive` hook will be triggered by Git and receive lines on standard input in the standard Git format: `<old-value> <new-value> <ref-name>\n`.
3. For every line read from stdin, the hook must append a single line of JSON to `/home/user/dashboard_data/push_events.jsonl`.
   * The directory `/home/user/dashboard_data` might not exist; your Rust program must create it if missing.
   * The JSON must have exactly this format: `{"event":"push","ref":"<ref-name>","new_commit":"<new-value>"}`
4. **Error Handling & Robustness:** If a line read from stdin does not contain exactly three space-separated fields, the Rust program must print "Invalid input" to standard error and exit with status code `1`.
5. **Permissions:** The Rust hook must ensure that the log file `/home/user/dashboard_data/push_events.jsonl` has exactly `644` (`rw-r--r--`) permissions after writing to it.

Do not assume any external Rust crates (like `serde` or `serde_json`) are available; you must format the JSON manually using standard library string manipulation. Ensure your final binary is natively compiled and placed in the correct hook path.