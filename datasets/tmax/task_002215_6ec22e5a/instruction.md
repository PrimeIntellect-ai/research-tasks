You are an on-call engineer who just received a critical page at 3:00 AM. The nightly metrics aggregation pipeline has crashed, and the downstream dashboards are completely empty.

You check the system and find that the main aggregation script, `/home/user/aggregate.sh`, failed to process today's metrics file `/home/user/data/metrics.txt`. The errors are recorded in `/home/user/cron.log`. 

The upstream service recently introduced some format edge-cases in the metrics payload: some metric values are now completely empty, while others might contain the string `NaN` when a subsystem is unreachable. 

Your tasks are:
1. **Analyze and Fix**: Read `/home/user/cron.log` to understand the crash. Modify `/home/user/aggregate.sh` so that it handles format parsing edge-cases gracefully. Specifically, any empty values or non-integer values (like `NaN`) must be treated as `0` during the sum aggregation. Ensure trailing/leading whitespaces around values do not break the script.
2. **Verify**: The script must correctly process `/home/user/data/metrics.txt` and output the final sum strictly in the format `Total: <number>`.
3. **Construct a Regression Test**: Create a regression test script at `/home/user/test_aggregate.sh` (make sure it is executable). This script must:
    - Create a temporary dummy metrics file containing at least one valid integer metric, one metric with an empty value, and one metric with a `NaN` value.
    - Run `/home/user/aggregate.sh` against this dummy file.
    - Verify that the output exactly matches the expected sum.
    - Exit with code `0` if the test passes, and exit with code `1` if the output is incorrect.

All your modifications and scripts must be written in Bash using standard coreutils.