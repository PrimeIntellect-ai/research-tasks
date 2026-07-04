You are a Linux Systems Engineer tasked with hardening and fixing a local health-check pipeline that monitors an internal service running inside a QEMU virtual machine.

Currently, the system is failing for three reasons:
1.  **Network Configuration:** The QEMU VM runs an echo service on TCP port 9000, but the host cannot reach it. The VM startup script at `/home/user/vm/start_vm.sh` is missing the necessary port forwarding configuration. You must modify this script so that host port 8080 forwards to the guest VM's port 9000, and then restart the VM.
2.  **Broken Cron Job:** A cron job executes a wrapper script `/home/user/healthcheck/wrapper.sh` every minute. This script is supposed to pipe system metrics through a sanitization program and send it to the VM service via `nc localhost 8080`. However, the cron job is failing because the wrapper script relies on commands that aren't in the restricted cron `PATH`. Fix the wrapper script so it executes correctly under cron.
3.  **Missing Sanitization Program:** The wrapper script calls a program named `sanitizer`, which does not exist. You must write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.

**Sanitizer Specification:**
Your C program must read from standard input (`stdin`) until EOF and write to standard output (`stdout`). It must act as a hardening filter with the following strict rules:
- Convert all uppercase alphabetical characters to lowercase.
- Replace any contiguous sequence of one or more non-alphanumeric characters (anything other than `a-z`, `A-Z`, and `0-9`) with a single underscore (`_`).
- If the input begins with a non-alphanumeric character, the resulting string must NOT start with an underscore (strip leading non-alphanumeric sequences).
- If the input ends with a non-alphanumeric character, the resulting string must NOT end with an underscore (strip trailing non-alphanumeric sequences).
- For example, `"Hello!!! WORLD?!  "` becomes `"hello_world"`. `"  123--AbC "` becomes `"123_abc"`.
- If the input contains only non-alphanumeric characters, the output should be completely empty.

**Tasks:**
1. Fix `/home/user/healthcheck/wrapper.sh` so it runs successfully in cron.
2. Modify `/home/user/vm/start_vm.sh` to forward host port 8080 to guest port 9000, and ensure the VM is running.
3. Write and compile `/home/user/sanitizer`.

Ensure all parts of the pipeline are functioning. The automated verification will intensely fuzz test your compiled `/home/user/sanitizer` binary against a secret oracle program to ensure absolute bit-exact compliance with the formatting rules. It will also trigger the cron job to verify the end-to-end data flow into the VM.