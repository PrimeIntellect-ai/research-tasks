You are an engineer investigating a memory leak in a long-running multi-language service. The service processes numerical data in a convergence loop, but a specific job recently crashed with an Out-Of-Memory (OOM) error. 

Before the service was killed, it generated two artifacts:
1. `/home/user/crash_trace.log`: The stack trace of the crash.
2. `/home/user/intermediate_state.bin`: A serialized state file dumped right before the crash.

Your investigation reveals that the system failed to converge, causing it to continuously allocate memory in a loop until it crashed. Furthermore, an internal debugging script trying to read `intermediate_state.bin` is failing because the file contains corrupted encoding (invalid UTF-8 bytes mixed into the serialization) due to a malformed job name.

Your task is to analyze these files and generate a JSON report.

You need to determine:
1. The exact name of the function where the convergence failure and memory leak occurred (based on the deepest application frame in the stack trace before the memory allocation calls).
2. The `target_threshold` that the convergence loop was trying to reach (this is stored as a 32-bit float at the very beginning of the `intermediate_state.bin` file, in little-endian format).
3. The recovered `job_name`. The job name is stored in `intermediate_state.bin` immediately following the 4-byte float. It is a corrupted UTF-8 string. You must recover the string by stripping out any non-ASCII bytes (keep only standard printable ASCII characters and alphanumeric characters).

Write your findings to `/home/user/debug_report.json` in exactly this format:
```json
{
  "failing_function": "function_name_here",
  "target_threshold": 0.0,
  "recovered_job_name": "JobNameHere"
}
```
Round the `target_threshold` to two decimal places in the JSON.