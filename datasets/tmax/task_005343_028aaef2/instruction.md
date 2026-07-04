You are tasked with fixing a critical pipeline regression that was tracked down during a recent 200-commit bisection. The regression causes statistical anomalies (impossible negative latency averages) and tracebacks in our query processing engine. 

Our pipeline consists of two separate services that currently aren't communicating due to a configuration gap:
1. **Emitter Service**: Runs in the background and exposes a stream of raw query logs on TCP port `8081`.
2. **Aggregator Service**: Listens for parsed logs on TCP port `8082` and computes real-time statistics.

Recently, malformed log entries started slipping into the pipeline. A normal log line looks like this:
`[TIMESTAMP] INFO: latency=45.2ms query="SELECT * FROM users"`

The malicious/malformed entries causing the regression have corrupted latency fields (e.g., negative values like `latency=-10.0ms` or non-numeric garbage like `latency=NaNms`). 

Your task consists of two parts:

**Part 1: The Sanitizer**
Create a bash shell script at `/home/user/sanitizer.sh` that acts as a stream filter.
- It must read lines from `stdin`.
- It must write valid lines to `stdout`.
- It must completely drop (reject) any line where the `latency=` value is negative (starts with `-`) or contains non-numeric/non-decimal characters (like `NaN`, `null`, etc.) before the `ms`.
- Do not modify valid lines.

To help you debug and verify your regex/logic, we have provided two directories containing log chunks:
- `/app/corpora/clean/` : Contains files with 100% valid logs. Your sanitizer must output these exactly as they are.
- `/app/corpora/evil/` : Contains files with tracebacks, injection attempts, and anomalous latency values. Your sanitizer must output absolutely nothing when fed these files.

**Part 2: The Glue**
Currently, the emitter and aggregator are disconnected. Create a bash script at `/home/user/run_bridge.sh` that connects them.
- It must continuously read the log stream from `localhost:8081`.
- It must pipe that stream through your `/home/user/sanitizer.sh` script.
- It must send the sanitized output directly into `localhost:8082`.
- You can use standard tools like `nc` (netcat) or bash sockets for this. 

Make sure both scripts are executable (`chmod +x`). Do not start the bridge in the background—the testing suite will execute `/home/user/run_bridge.sh` when it's ready to test the end-to-end flow.