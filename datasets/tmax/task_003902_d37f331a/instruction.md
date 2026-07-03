You are a security engineer tasked with auditing and rotating credentials for a legacy authentication service. The old service binary is being deprecated because it contains a hardcoded fallback credential that has been leaked.

Before we can complete the credential rotation and shut down the service, you need to identify which IP addresses have been actively exploiting this fallback credential, and sanitize our access logs to prevent further exposure of the leaked key.

Your task consists of the following steps:

1. **Extract the Leaked Credential:**
   Analyze the legacy ELF binary located at `/home/user/legacy_auth`. The hardcoded fallback credential is a string stored in the read-only data section (`.rodata`) and always begins with the prefix `FBK_`. Use binary analysis or reverse engineering tools to find the exact value of this credential.

2. **Process Security Logs using Rust:**
   Create a new Rust Cargo project at `/home/user/log_processor`. Write a Rust program that reads the security log file located at `/home/user/auth_events.log`.

   The log file contains entries in the following format:
   `[TIMESTAMP] IP=<ip_address> status="<status>" cred="<credential>"`

3. **Identify Intrusions:**
   Your Rust program must parse the logs and identify all unique IP addresses that had a successful authentication (`status="SUCCESS"`) using the leaked fallback credential you extracted in Step 1.
   Write these unique IP addresses to `/home/user/compromised_ips.txt`, with one IP address per line, sorted in ascending alphabetical order.

4. **Redact Sensitive Data:**
   Your Rust program must also create a sanitized version of the log file at `/home/user/redacted_auth_events.log`. In this new file, every occurrence of the exact leaked fallback credential must be replaced with the string `[REDACTED_CRED]`. All other content in the logs should remain exactly the same.

Ensure your Rust project compiles and runs successfully, producing the two required output files (`compromised_ips.txt` and `redacted_auth_events.log`). You can use any standard Rust crates (like `regex` or `lazy_static`) by adding them to your `Cargo.toml`.