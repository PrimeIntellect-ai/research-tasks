You are an automation specialist tasked with fixing and enhancing a Bash-based stream processing pipeline. We have a set of mock services that handle log ingestion, but they are disconnected, and the firewall component is missing. 

Your objectives are twofold:

1. **Service Composition:**
There are three services in `/app/services/`:
- `receiver.sh`: Listens on a TCP port for incoming logs and outputs them to stdout.
- `aggregator.sh`: Reads from stdin and calculates rolling aggregations, saving the output.
- `start_pipeline.sh`: A script that is supposed to launch `receiver.sh` on port `9090`, pipe its output into your custom `firewall.sh` (which you will create), and pipe that output into `aggregator.sh`.
Currently, `start_pipeline.sh` is misconfigured and doesn't link the streams properly. You must fix `/app/services/start_pipeline.sh` so that data flows perfectly from receiver -> firewall -> aggregator.

2. **Data Sanitization and Filtering (`firewall.sh`):**
You must write a script at `/home/user/firewall.sh` (executable) that processes lines from standard input to standard output using Bash, Awk, Sed, and standard coreutils.

Each log line is a pipe-separated string: `TIMESTAMP|IP|USERNAME|MESSAGE`
For example: `2023-10-12T10:05:01Z|192.168.1.10|JohnDoe|Login successful`

The `firewall.sh` must:
- **Anonymize PII:** Replace any 9-digit US Social Security Numbers (format `XXX-XX-XXXX`) in the MESSAGE field with `***-**-****`.
- **Unicode Normalization:** Strip all zero-width spaces (U+200B, which is `\xE2\x80\x8B` in UTF-8) from the USERNAME field.
- **Timestamp Alignment:** If the timestamp is missing the timezone 'Z' at the end but is otherwise ISO-8601, append the 'Z'. (e.g., `2023-10-12T10:05:01` becomes `2023-10-12T10:05:01Z`).
- **Rolling Window Rate Limiting:** Maintain a rolling window of 10 seconds. If a single IP address generates more than 3 logs within any 10-second window, drop the 4th log and all subsequent logs from that IP until the window clears. (Use the log's TIMESTAMP, not system time, assuming logs are chronological).

You can test your `firewall.sh` against the corpora in `/home/user/corpora/`.
- `/home/user/corpora/clean/`: Contains logs that must pass through `firewall.sh` completely unchanged.
- `/home/user/corpora/evil/`: Contains logs with PII, bad unicode, bad timestamps, and spamming IPs. Your script must correctly sanitize or drop these lines.

Ensure `firewall.sh` flushes its output line-by-line so it works in a real-time stream.