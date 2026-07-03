You are tasked with investigating a critical memory and goroutine leak in our production Go service. The service occasionally leaks goroutines when certain requests are cancelled, eventually crashing the node.

You have been provided with an alert dashboard screenshot at `/app/alert.png`.
1. Analyze `/app/alert.png` (using `tesseract` or similar tools) to extract the primary "Trace ID" of the incident.
2. In `/app/telemetry/`, there is a damaged SQLite database `logs.db` containing the telemetry and goroutine dumps for various requests. You must recover the corrupted database to extract the records. 
3. Locate the row in the recovered database corresponding to the extracted Trace ID. This row contains a full pprof goroutine dump that captures the leak in progress.
4. Analyze the goroutine dump to understand the root cause of the leak. You are looking for a specific cancellation bug where a goroutine is permanently blocked on channel send because the parent context was cancelled and the receiver stopped listening.
5. Once you have identified the exact signature of this leak (the specific blocking function in our application code, e.g., `github.com/company/srv/worker.processTask`), build a Go CLI detector.

Write a Go program and compile it to `/home/user/detector`.
Your program must accept a single argument: the path to a plain-text file containing a goroutine dump.
Usage: `/home/user/detector <path_to_dump_file>`

- If the dump contains the specific goroutine leak (a goroutine stuck in the buggy function due to the cancellation bug), your program MUST exit with status code `1` (Reject).
- If the dump is from normal traffic or unrelated errors, your program MUST exit with status code `0` (Accept).

Our automated verifier will run your compiled `/home/user/detector` against two hidden corpora of goroutine dumps. To pass, your detector must achieve 100% accuracy on both the clean and leaky datasets.