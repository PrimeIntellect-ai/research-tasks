You are a monitoring specialist setting up a new alerting pipeline. 

We have a legacy, proprietary binary at `/app/log_oracle` that validates incoming alert payloads. However, this binary is interactive (it prompts for a passphrase), extremely slow, and cannot be used in our real-time logging pipeline. We need a fast replacement written in Rust.

Your tasks are:

1. **Investigate the Oracle:**
   The binary `/app/log_oracle` is a stripped executable. When run with a file path as an argument (e.g., `/app/log_oracle payload.json`), it prompts for a passphrase. (Hint: The passphrase is `monitor_auth_99`). After receiving the passphrase, it will evaluate the payload and output either `[VALID]` or `[REJECT]`. 
   Write an `expect` script or use basic reverse engineering to analyze how `/app/log_oracle` classifies files. You have some sample alerts in `/app/corpus_samples/clean/` and `/app/corpus_samples/evil/` to help you deduce the validation rules.

2. **Develop the Rust Filter:**
   Write a Rust program at `/home/user/alert_filter.rs` and compile it to `/home/user/alert_filter`. 
   - The program must take exactly one argument: the path to an alert JSON file.
   - It must implement the exact same validation logic as `/app/log_oracle`.
   - If the alert is valid, it must exit with status code `0`.
   - If the alert is invalid (malicious/malformed), it must exit with status code `1`.

3. **Configuration & ACLs:**
   Create a configuration file for your filter at `/home/user/filter.toml` containing:
   ```toml
   [filter]
   strict_mode = true
   ```
   Using Access Control Lists (ACLs), grant the `nobody` user read-only access to this specific file, ensuring the base permissions do not grant access to "others" (`chmod o-rwx`).

Ensure your Rust binary is compiled and placed exactly at `/home/user/alert_filter` before finishing.