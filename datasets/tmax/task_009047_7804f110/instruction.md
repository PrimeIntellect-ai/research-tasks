You are an on-call infrastructure engineer. It's 3:00 AM UTC, and you've just been paged. The daily metric aggregation pipeline, which runs a critical Bash script, is failing and preventing downstream services from updating.

The incident report states:
"The aggregation pipeline script `/home/user/pipeline/aggregate.sh` is abruptly failing. The C helper binary it calls (`calc_stats`) is crashing with a Floating Point Exception (SIGFPE) and dumping a stack trace to the console. The pipeline relies on processing yesterday's logs, but something is causing the time deltas to be calculated incorrectly, leading to a fatal crash."

Your investigation should focus on:
1. **Core dump / Stack trace analysis**: Review the stack trace produced by `calc_stats` when running the pipeline to understand where and why it crashes.
2. **Intermediate state tracing**: Add debugging (e.g., `set -x` or `echo`) to `/home/user/pipeline/aggregate.sh` to trace the intermediate state of the variables being passed to the helper.
3. **Precision loss tracking**: The pipeline calculates event durations from log timestamps. Identify where precision is being lost in the Bash arithmetic and fix it.
4. **Timezone bugs**: The pipeline is supposed to process logs for the current UTC day (since it runs at 3 AM UTC), but a timezone offset is causing it to fetch the wrong data or calculate negative/zero time spans.

**Tasks:**
1. Execute `/home/user/pipeline/aggregate.sh` to observe the failure.
2. Debug and fix the `/home/user/pipeline/aggregate.sh` script. You must modify the script to:
   - Use the correct timezone (UTC) for determining the current log file date.
   - Prevent precision loss when calculating the duration in seconds (the helper binary expects a floating-point string with at least 3 decimal places, e.g., `0.045`, not `0`).
3. Once fixed, run `/home/user/pipeline/aggregate.sh`. It will automatically generate `/home/user/pipeline/output.txt`.
4. Copy the final calculated metric from `/home/user/pipeline/output.txt` and write it to `/home/user/resolution.txt` exactly as a single floating point number.

**Environment details:**
- Pipeline directory: `/home/user/pipeline/`
- Logs directory: `/home/user/logs/`