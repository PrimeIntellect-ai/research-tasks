You are a DevSecOps engineer tasked with enforcing policy as code for a sensitive log-processing pipeline. 

An application processes credit card transactions and logs communication events. Due to recent security policy updates, you must automatically identify traffic to domains that failed TLS certificate chain validation, extract those domain's logs, and redact any sensitive credit card numbers before sharing the logs with the development team. Furthermore, because the log parser handles potentially malicious input, it must be executed in an isolated sandbox.

You need to create two Bash scripts in `/home/user/`:

1. `/home/user/parse_logs.sh`:
   - Reads a log file specified as the first argument.
   - Parses the log to find any domain that has a `CERT_CHAIN_FAIL` event.
   - Extracts ALL log entries (before and after) that belong to these specific failed domains.
   - Redacts any 16-digit credit card numbers matching the pattern `\d{4}-\d{4}-\d{4}-\d{4}` by replacing them entirely with `XXXX-XXXX-XXXX-XXXX`.
   - Writes the correlated and redacted lines to `/home/user/output/redacted_failed.log` in the same chronological order they appeared.

2. `/home/user/run_sandbox.sh`:
   - A wrapper script that executes `/home/user/parse_logs.sh /home/user/app_logs/server.log` using `bwrap` (Bubblewrap) to enforce process isolation.
   - The sandbox must enforce the following policies:
     - Mount the root filesystem `/` as read-only.
     - Mount `/dev` appropriately (e.g., `--dev /dev`).
     - Bind mount `/home/user/output/` with read-write access so the script can write the output file.
     - Unshare all namespaces (network, pid, ipc, etc.) using `--unshare-all`.

**Log Format Example:**
```
2023-10-01T10:00:01 INFO [api.badsite.com] Request received user=bob cc=4111-2222-3333-4444
2023-10-01T10:00:02 ERROR [api.badsite.com] CERT_CHAIN_FAIL Issuer unknown
2023-10-01T10:00:03 INFO [secure.vendor.com] Request received user=alice cc=5555-6666-7777-8888
2023-10-01T10:00:04 INFO [secure.vendor.com] CERT_VALIDATION_SUCCESS
```

**Directories and setup:**
- The input logs are located at `/home/user/app_logs/server.log`.
- You must create the output directory `/home/user/output/`.
- Once your scripts are ready, execute `/home/user/run_sandbox.sh` to generate the final log file.