You are a monitoring specialist tasked with setting up an automated alerting and security configuration system. You need to write a Rust-based log scanner, automate an interactive legacy mail tool using `expect`, and write an idempotent configuration script for our mock firewall.

Here are the specific requirements:

**Phase 1: Automating the Legacy Mailer**
There is a legacy interactive mailing script located at `/home/user/legacy_mailer.py`. When executed, it prompts exactly as follows:
1. `Recipient:`
2. `Subject:`
3. `Message:`
4. `Send? (y/n):`

Write an `expect` script at `/home/user/send_alert.exp` that automates this interaction.
- The script should accept three command-line arguments: `recipient`, `subject`, and `message`.
- It should answer `y` to the final confirmation prompt.
- Make sure the script is executable.

**Phase 2: Rust Log Scanner**
Create a Rust project in `/home/user/log_monitor`.
Write a CLI tool that takes a log file path as its first argument.
- It must read the file line by line.
- For every line that contains the exact substring `[CRITICAL]`, the Rust program must execute your `/home/user/send_alert.exp` script.
- The arguments passed to the `expect` script should be:
  - Recipient: `oncall@local.domain`
  - Subject: `Critical System Alert`
  - Message: The exact matching log line.
- Compile the program in release mode so the binary is available at `/home/user/log_monitor/target/release/log_monitor`.

**Phase 3: Idempotent Firewall Configuration**
Write a bash script at `/home/user/config_fw.sh` that acts as an idempotent configuration manager for our port forwarding and firewall rules.
- The script should maintain a configuration file at `/home/user/firewall.conf`.
- It must ensure the following two rules are present in the file:
  - `FORWARD PORT 8080 TO 9090`
  - `BLOCK PORT 22`
- **Crucial:** The script must be idempotent. If run 1 time or 100 times, `/home/user/firewall.conf` must contain exactly one instance of each rule, and no other lines (unless added by other processes, which it should not disturb). Do not use `sudo`.

Your tasks are to write `/home/user/send_alert.exp`, implement and build the Rust project at `/home/user/log_monitor`, and write `/home/user/config_fw.sh`.