You are a Site Reliability Engineer (SRE) monitoring uptime for your company's critical infrastructure. The uptime monitoring service, written in Rust, recently crashed while processing the latest batch of metric logs. 

You have been provided with the following files in your home directory (`/home/user`):
1. `raw_metrics.log` - The raw metric logs the service was processing before it crashed.
2. `uptime_monitor.log` - The service's stdout/stderr log, which contains the Rust panic traceback.
3. `memory.dmp` - A raw binary memory dump of the specific data structure that caused the panic, dumped by the service's crash handler right before termination.

Your task is to:
1. Analyze the traceback in `uptime_monitor.log` and the memory dump in `memory.dmp` to identify the exact corrupt `metric_id` string that caused the crash.
2. Write a Rust script at `/home/user/cleaner.rs` that reads `/home/user/raw_metrics.log`, filters out any log lines containing the corrupt `metric_id`, and writes the valid lines to `/home/user/cleaned_metrics.log` in the exact same order and format.
3. Compile and run your `cleaner.rs` script.
4. Generate a unified diff between the original logs and the cleaned logs by running `diff -u /home/user/raw_metrics.log /home/user/cleaned_metrics.log > /home/user/metrics.diff` (it is expected that diff will return an exit code of 1; this is fine).
5. Save the exact corrupt `metric_id` string to a file named `/home/user/bad_metric.txt`.

Ensure all requested files (`cleaner.rs`, `cleaned_metrics.log`, `metrics.diff`, `bad_metric.txt`) are present in `/home/user/`.