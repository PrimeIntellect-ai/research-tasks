You are acting as a Site Reliability Engineer (SRE). Our internal monitoring service, an agent written in Rust, has suddenly started crashing, and we've also lost the legacy API authentication key required to report metrics.

Here is the situation:
1. The source code for the monitoring agent is located at `/home/user/uptime-monitor`.
2. The agent processes a list of endpoints from `/home/user/uptime-monitor/endpoints.json`. However, when you run `cargo run -- process endpoints.json`, it panics. We suspect one specific endpoint configuration is triggering a bug in the data transformation logic, but there are hundreds of endpoints in the file.
3. Furthermore, the service is currently unauthorized because the `API_KEY` environment variable is missing. A junior developer accidentally committed the plaintext API key into the git repository a few commits ago, and then tried to hide it by removing it in a subsequent commit.

Your tasks are:
1. **Git Forensics**: Search the git history of the `/home/user/uptime-monitor` repository to recover the leaked legacy API key.
2. **Delta Debugging**: Isolate the exact endpoint in `endpoints.json` that causes the Rust application to panic. You must find the `id` of this failing endpoint.
3. **Fix the Bug**: Modify `src/main.rs` to gracefully handle the invalid data transformation (e.g., return an error or skip the endpoint) instead of panicking. Run `cargo build` to ensure your fix compiles successfully.
4. **Report Verification**: Create a JSON file at `/home/user/resolution.json` with the exact following structure containing your findings:

```json
{
  "recovered_api_key": "<the exact API key string found in git history>",
  "failing_endpoint_id": "<the string ID of the endpoint causing the panic>"
}
```

Make sure the keys in the JSON exactly match what is requested, and the repository compiles cleanly after your fix.