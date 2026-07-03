You are a monitoring specialist tasked with setting up an automated alert system for a legacy virtual machine. 

We have a simulated QEMU wrapper script located at `/home/user/bin/mock_qemu`. During its startup, this legacy VM pauses at the bootloader and requires a manual keypress ('c') via the serial console to continue booting. If it does not receive this input, it eventually times out and crashes with a kernel panic.

Your task is to fully automate the monitoring of this boot process using a combination of Expect, Rust, and cron.

Perform the following tasks:

1. **Expect Script**:
   Create an Expect script at `/home/user/check_vm.exp`. This script must:
   - Execute the `/home/user/bin/mock_qemu` command.
   - Wait for the exact prompt: `Press 'c' to continue boot...`
   - Send the character `c` followed by a carriage return or newline.
   - Wait for the command to finish and exit cleanly, printing the final output to stdout.

2. **Rust Monitoring Agent**:
   Create a new Rust binary project in the directory `/home/user/vm_monitor/`. 
   Write a Rust program that:
   - Executes the Expect script `/home/user/check_vm.exp` as a child process.
   - Captures its standard output.
   - If the output contains the string `BOOT SUCCESS`, the program should exit with code 0 without doing anything else.
   - If the output contains the string `KERNEL PANIC` or if the Expect script fails/times out, the Rust program must append exactly the line `ALERT: VM boot failed` to the file `/home/user/alerts.log` (create the file if it does not exist) and then exit with code 0.
   - Compile the Rust project so that the binary is available at `/home/user/vm_monitor/target/debug/vm_monitor`.

3. **Cron Scheduling**:
   Create a crontab configuration file at `/home/user/monitor_cron`. 
   This file should contain exactly one cron job that schedules your compiled Rust binary (`/home/user/vm_monitor/target/debug/vm_monitor`) to run every 5 minutes. 
   Assume standard cron syntax (e.g., `* * * * * command`).

Constraints:
- Do not use `sudo` or modify system-wide files.
- The Rust program must successfully compile using `cargo build`.
- You may use standard Rust libraries (e.g., `std::process::Command`, `std::fs::OpenOptions`, `std::io::Write`). No external crates are strictly required.